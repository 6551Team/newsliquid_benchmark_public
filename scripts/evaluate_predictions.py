from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import Any


LABELS = ["long", "short", "neutral"]
INVALID_DIRECTION = "__invalid__"
EPSILON = 0.0001
MAX_IMPACT_ERROR = 100


def main() -> None:
    parser = argparse.ArgumentParser(description="Score FinTech News Impact Benchmark predictions.")
    parser.add_argument("--predictions", type=Path, required=True, help="JSONL with id, direction, impact_score, and optional latency_ms.")
    parser.add_argument("--labels", type=Path, default=Path(__file__).resolve().parents[1] / "data" / "reference_labels.jsonl")
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Debug only: score the matched subset instead of requiring all benchmark rows.",
    )
    args = parser.parse_args()

    refs = {row["id"]: row for row in read_jsonl(args.labels)}
    preds = read_jsonl(args.predictions)
    rows = []
    seen_ids = set()
    duplicate_ids = []
    unknown_ids = []
    for pred in preds:
        pred_id = pred.get("id")
        if pred_id in seen_ids:
            duplicate_ids.append(str(pred_id))
            continue
        seen_ids.add(pred_id)

        ref = refs.get(pred_id)
        if not ref:
            unknown_ids.append(str(pred_id))
            continue

        direction, direction_valid = parse_direction(pred.get("direction"))
        impact, impact_valid = parse_impact(pred.get("impact_score"), 0, 100)
        valid_output = direction_valid and impact_valid
        ref_impact = int(ref["impact_score"])
        rows.append(
            {
                "id": pred_id,
                "pred_direction": direction if valid_output else INVALID_DIRECTION,
                "pred_impact": impact,
                "direction_valid": direction_valid,
                "impact_valid": impact_valid,
                "valid_output": valid_output,
                "ref_direction": ref["direction"],
                "ref_impact": ref_impact,
                "impact_error": abs(impact - ref_impact) if impact_valid and impact is not None else MAX_IMPACT_ERROR,
                "latency_ms": to_float(pred.get("latency_ms")),
            }
        )

    if duplicate_ids:
        preview = ", ".join(duplicate_ids[:10])
        raise SystemExit(f"Duplicate prediction ids are not allowed: {preview}")

    matched_ids = {row["id"] for row in rows}
    missing_ids = sorted(set(refs) - matched_ids)
    if (missing_ids or unknown_ids) and not args.allow_partial:
        raise SystemExit(
            "Prediction file must contain exactly one prediction for every benchmark row; "
            f"matched={len(rows)} expected={len(refs)} missing={len(missing_ids)} unknown={len(unknown_ids)}"
        )

    if not rows:
        raise SystemExit("No prediction rows matched the reference labels.")

    latencies = [row["latency_ms"] for row in rows if row["latency_ms"] is not None]
    direction_accuracy = mean([row["pred_direction"] == row["ref_direction"] for row in rows])
    macro = macro_f1(rows)
    mae = statistics.mean(row["impact_error"] for row in rows)
    output_accuracy = (direction_accuracy + macro) / 2
    qps = 1000.0 / statistics.mean(latencies) if latencies else None
    score = qps * (-math.log2(1 - output_accuracy + EPSILON)) if qps else None
    invalid_output_count = sum(1 for row in rows if not row["valid_output"])

    print(
        json.dumps(
            {
                "n": len(rows),
                "expected_rows": len(refs),
                "partial_debug": bool(args.allow_partial),
                "missing_count": len(missing_ids),
                "unknown_id_count": len(unknown_ids),
                "invalid_output_count": invalid_output_count,
                "invalid_direction_count": sum(1 for row in rows if not row["direction_valid"]),
                "invalid_impact_score_count": sum(1 for row in rows if not row["impact_valid"]),
                "direction_accuracy": direction_accuracy,
                "macro_f1": macro,
                "impact_mae": mae,
                "output_accuracy": output_accuracy,
                "mean_news_latency_ms": statistics.mean(latencies) if latencies else None,
                "p99_news_latency_ms": percentile(sorted(latencies), 99) if latencies else None,
                "qps": qps,
                "score_bits_per_second": score,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def macro_f1(rows: list[dict[str, Any]]) -> float:
    f1s = []
    for label in LABELS:
        tp = sum(1 for row in rows if row["ref_direction"] == label and row["pred_direction"] == label)
        fp = sum(1 for row in rows if row["ref_direction"] != label and row["pred_direction"] == label)
        fn = sum(1 for row in rows if row["ref_direction"] == label and row["pred_direction"] != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1s.append((2 * precision * recall / (precision + recall)) if precision + recall else 0.0)
    return statistics.mean(f1s)


def parse_direction(value: Any) -> tuple[str | None, bool]:
    value = str(value or "").strip().lower()
    if value in LABELS:
        return value, True
    return None, False


def parse_impact(value: Any, low: int, high: int) -> tuple[int | None, bool]:
    try:
        numeric = float(value)
    except Exception:
        return None, False
    if not math.isfinite(numeric):
        return None, False
    parsed = int(round(numeric))
    if parsed < low or parsed > high:
        return None, False
    return parsed, True


def to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except Exception:
        return None


def mean(values: list[bool]) -> float:
    return sum(1 for value in values if value) / len(values) if values else 0.0


def percentile(ordered: list[float], pct: float) -> float:
    if not ordered:
        return 0.0
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * pct / 100
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    weight = pos - lo
    return ordered[lo] * (1 - weight) + ordered[hi] * weight


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


if __name__ == "__main__":
    main()

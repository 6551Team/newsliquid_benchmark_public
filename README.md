# FinTech News Impact Benchmark v1

A single-news benchmark for measuring how fast and accurately a model can judge the likely market impact of financial technology news on a target asset.

This public release is a human-annotated benchmark test set. The reference labels in `data/reference_labels.jsonl` are the official benchmark labels for scoring.

**Disclosure:** 6551 News Research both maintains this benchmark and submits the in-house `newsliquid-1.0-flash` entry. That entry is marked with `†` in the leaderboard and should be interpreted with this conflict of interest in mind.

## Files

- `data/test_public.jsonl`: public input set without labels.
- `data/reference_labels.jsonl`: human-annotated benchmark test-set labels for scoring.
- `data/benchmark_with_reference.jsonl`: audit-only merge of inputs and reference labels. Do not use this file for inference or leaderboard evaluation.
- `results/leaderboard.csv`: current measured public-board results.
- `docs/EVALUATION_PROTOCOL.md`: scoring and runtime rules.
- `docs/ANNOTATION_GUIDE.md`: label definitions and review checklist.
- `docs/SCHEMA.md`: data-field definitions and release notes.
- `docs/SUBMISSION_FORMAT.md`: required prediction-file format.
- `examples/sample_predictions.jsonl`: small format example for submissions. It is not a complete scorable submission.
- `scripts/evaluate_predictions.py`: local scoring helper for a submitted prediction file.

## Folder Layout

```text
.
|-- README.md
|-- DATASET_CARD.md
|-- LEADERBOARD.md
|-- leaderboard_release.html
|-- LICENSE
|-- CITATION.cff
|-- data/
|   |-- test_public.jsonl
|   |-- test_public.csv
|   |-- reference_labels.jsonl
|   |-- reference_labels.csv
|   |-- benchmark_with_reference.jsonl
|   `-- metadata.json
|-- docs/
|   |-- ANNOTATION_GUIDE.md
|   |-- EVALUATION_PROTOCOL.md
|   |-- SCHEMA.md
|   `-- SUBMISSION_FORMAT.md
|-- examples/
|   `-- sample_predictions.jsonl
|-- results/
|   |-- leaderboard.json
|   `-- leaderboard.csv
`-- scripts/
    `-- evaluate_predictions.py
```

## Task

Given one news item and one target asset, output:

```json
{"direction":"long|short|neutral","impact_score":0-100}
```

`impact_score` measures event strength, not realized future return.

## Current Size

- Rows: 200
- Direction distribution: {"short": 45, "long": 99, "neutral": 56}
- Buckets: {"important": 129, "random": 71}

## Public-Board Rule

All submissions must run one news item per request, with batching and response caching disabled. Use `data/test_public.jsonl` for inference. Hidden labels should be loaded only after predictions have been written. `data/benchmark_with_reference.jsonl` includes labels and is for audit/analysis only.

## Honest Scope Notes

This benchmark includes latency in the score, so the result is not a pure model-quality ranking. Network jitter, provider routing, local hardware, GPU load, and runtime configuration can move latency numbers. The goal is to provide a practical scoring standard for financial-news systems that must balance timeliness and accuracy, measured under the most consistent environment we can maintain.

`newsliquid-1.0-flash` is optimized for low-latency news triage. Its output accuracy is below the strongest general-purpose frontier models on this benchmark, which is an intentional speed/accuracy tradeoff. In weakly time-sensitive workflows, users should consider routing uncertain or high-value items to a stronger model for second-pass verification.

## Local Scoring

```bash
python scripts/evaluate_predictions.py --predictions path/to/predictions.jsonl
```

The scorer uses only the Python standard library. A leaderboard submission should contain predictions for all 200 public IDs.

The bundled `examples/sample_predictions.jsonl` contains only a few rows and is for format inspection. To score that sample for debugging, use:

```bash
python scripts/evaluate_predictions.py --predictions examples/sample_predictions.jsonl --allow-partial
```

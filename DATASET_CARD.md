# Dataset Card

## Dataset Summary

FinTech News Impact Benchmark v1 contains timestamped financial technology news items with a target asset and reference impact labels.

## Intended Use

- Compare models on direction classification, impact scoring, and single-news latency.
- Evaluate public leaderboard submissions under a no-batch, no-cache protocol.
- Use `data/test_public.jsonl` for inference and evaluation. `data/benchmark_with_reference.jsonl` contains labels and is for audit or offline analysis only.

## Conflict Disclosure

6551 News Research both maintains this benchmark and submits the in-house `newsliquid-1.0-flash` leaderboard entry. Readers should interpret that entry with this conflict of interest in mind.

## Label Schema

- `long`: the news is bullish for the target asset.
- `short`: the news is bearish for the target asset.
- `neutral`: the news is weak, indirect, ambiguous, or mostly background for the target asset.
- `impact_score`: 0-100 event-strength score.

## Composition

- Rows: 200
- Direction counts: {"short": 45, "long": 99, "neutral": 56}
- Category counts: {"exchange_listing_delisting": 32, "regulation_legal_etf": 34, "security_risk": 22, "rating_high_other": 50, "market_stress": 33, "tokenomics_protocol": 21, "macro_institutional": 8}

## Annotation Status

This release is a human-annotated benchmark test set. The reference labels are the official benchmark scoring labels, and label rationales are kept short and event-focused. The annotation policy is documented in `docs/ANNOTATION_GUIDE.md`.

Reference-label `reason` fields are written in Simplified Chinese. The English HTML report includes translated worked examples, but the shipped JSONL/CSV labels preserve the original concise analyst notes.

## Data Fields

Field definitions for `test_public.jsonl`, `reference_labels.jsonl`, `benchmark_with_reference.jsonl`, metadata files, and result files are documented in `docs/SCHEMA.md`.

Source names and `news_type` values preserve the raw feed values and casing. For example, `Coindesk` and `coindesk` are separate source strings in the metadata counts because they came from different feed records; the release does not case-normalize them.

## Limitations

- Latency-aware scores are sensitive to network and serving conditions; repeat runs should report the environment and date.
- The dataset is focused on short-horizon financial technology news impact and should not be treated as a general financial reasoning benchmark.
- The benchmark evaluates immediate event interpretation, not realized trading profitability or future K-line movement.
- Fast specialist models may rank highly by information rate while still trailing larger models in pure output accuracy.
- For low-urgency or high-stakes workflows, a second-pass review by a stronger model or a human analyst is recommended.

## Content Rights

News text and links may originate from third-party sources. Check redistribution terms before publishing the full-text files outside the project.

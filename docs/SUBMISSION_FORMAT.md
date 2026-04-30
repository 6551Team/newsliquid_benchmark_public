# Submission Format

Submissions are JSONL files with one JSON object per benchmark row.

## Required Fields

- `id`: benchmark row ID, matching `data/test_public.jsonl`.
- `direction`: one of `long`, `short`, or `neutral`.
- `impact_score`: integer or numeric value from 0 to 100.

Rows with missing, unknown, or unparsable required fields are invalid. Invalid rows count as wrong predictions in the scorer.

## Optional Field

- `latency_ms`: end-to-end single-news latency in milliseconds. Include this field for latency-aware leaderboard scoring.

## Rules

1. Include predictions for all 200 public IDs.
2. Process exactly one news item per request.
3. Do not batch requests.
4. Do not cache or reuse previous outputs.
5. Do not read `data/reference_labels.jsonl` until predictions have been written.

## Example

The following file is a format example only. It contains three rows, not a complete leaderboard submission.

```jsonl
{"id":"cnib-v1-0001","direction":"short","impact_score":90,"latency_ms":142.7}
{"id":"cnib-v1-0002","direction":"long","impact_score":85,"latency_ms":139.4}
{"id":"cnib-v1-0003","direction":"neutral","impact_score":25,"latency_ms":141.9}
```

Score a complete prediction file with:

```bash
python scripts/evaluate_predictions.py --predictions path/to/predictions.jsonl
```

For local format debugging on a partial file, use:

```bash
python scripts/evaluate_predictions.py --predictions examples/sample_predictions.jsonl --allow-partial
```

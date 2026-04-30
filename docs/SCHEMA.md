# Data Schema

## `data/test_public.jsonl`

Each row is one public benchmark input without reference labels.

- `id`: stable public row ID.
- `timestamp`: source timestamp string as captured in the feed.
- `source`: raw source label from the feed. Casing is preserved and not normalized.
- `news_type`: raw feed subtype or source channel.
- `engine_type`: upstream feed family such as `news`, `market`, `prediction`, `onchain`, `kol`, or `meme`.
- `target_asset`: asset or market identifier the model should evaluate.
- `symbols`: source-provided symbol list.
- `title`: source headline or short event title.
- `text`: full text or source event body supplied to the benchmark.
- `text_length`: character count of `text` at packaging time.
- `link`: source URL when available.
- `sample_bucket`: `important` or `random`, indicating sampling bucket.
- `category`: benchmark category used for composition analysis.

## `data/reference_labels.jsonl`

Each row is the official human-annotated benchmark test-set label for one public ID.

- `id`: benchmark row ID.
- `target_asset`: target asset copied from the input row.
- `direction`: one of `long`, `short`, or `neutral`.
- `impact_score`: integer 0-100 event-strength score.
- `confidence`: annotator confidence on a 0-100 scale.
- `label`: compact label in `[L|S|N][0-100]` format.
- `reason`: concise analyst rationale in Simplified Chinese.

## `data/benchmark_with_reference.jsonl`

Audit-only merge of `test_public.jsonl` and `reference_labels.jsonl`. Each row contains all public input fields plus a nested `reference` object. Do not use this file for inference or leaderboard evaluation because it exposes the labels.

## Metadata And Results

- `data/metadata.json`: canonical benchmark metadata and composition counts.
- `results/leaderboard.json`: leaderboard result file with a copied benchmark metadata snapshot for portability.
- `results/leaderboard.csv`: compact table version of the leaderboard.

## Normalization Notes

The release preserves raw feed strings in the input rows. Source counts are intentionally not case-normalized; for example, `Coindesk` and `coindesk` remain separate source values if they appeared that way in the source feed.

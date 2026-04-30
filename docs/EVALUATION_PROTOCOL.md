# Evaluation Protocol

## Inference Rules

1. Process exactly one news item per request.
2. Disable batching, response caching, and reuse of previous outputs.
3. Do not read reference labels until all predictions have been written.
4. Record end-to-end latency for every news item.
5. Count invalid or unparsable outputs as wrong predictions.
6. Report serving location, provider route, hardware class, and run date when publishing new leaderboard entries.
7. Use `data/test_public.jsonl` for inference. `data/benchmark_with_reference.jsonl` contains labels and is for audit only.

## Metrics

- Direction accuracy
- Macro F1 across `long`, `short`, `neutral`
- MAE for impact score audit
- Mean and P99 news latency
- QPS = `1000 / mean_news_latency_ms`
- Output accuracy = `(direction_accuracy + macro_f1) / 2`
- Score bits/s = `QPS * [-log2(1 - output_accuracy + 0.0001)]`

Invalid `direction` values, missing `direction`, missing `impact_score`, unparsable `impact_score`, or out-of-range `impact_score` values make that row invalid. Invalid rows count as wrong for direction accuracy and Macro F1. Invalid impact scores receive the maximum MAE audit penalty.

## Interpretation Notes

Latency is part of this benchmark because financial-news systems often lose value when the interpretation arrives too late. This also means the leaderboard is sensitive to networking and serving conditions. Results should be read as a practical throughput-and-accuracy comparison under a stated environment, not as an immutable model-quality score.

A low-latency model can outperform a more accurate model on the information-rate score if it returns usable predictions much faster. That tradeoff is intentional. For workflows where speed is less important than precision, use output accuracy, Macro F1, and a second-pass verification policy instead of relying only on the combined score.

# Leaderboard

**Disclosure:** 6551 News Research both maintains this benchmark and submits the in-house `newsliquid-1.0-flash` entry. The `†` marker denotes this conflict of interest.

| Rank | Score bits/s | Model | Output Accuracy | Mean News Latency ms | P99 News Latency ms | QPS |
|---:|---:|---|---:|---:|---:|---:|
| 1 | 13.290 | newsliquid-1.0-flash †[^coi] | 72.5% | 140.1 | 226.2 | 7.140 |
| 2 | 6.530 | qwen/qwen3.6-35b-a3b | 86.3% | 438.9 | 1075.8 | 2.279 |
| 3 | 6.479 | zai-org/glm-4.7-flash | 76.4% | 321.1 | 445.9 | 3.114 |
| 4 | 2.986 | qwen3-4b | 60.0% | 442.2 | 542.4 | 2.262 |
| 5 | 1.983 | gpt-5.4-nano | 83.8% | 1325.1 | 2977.0 | 0.755 |
| 6 | 1.942 | gpt-5.5 | 92.8% | 1949.2 | 3332.3 | 0.513 |
| 7 | 1.887 | claude-haiku-4.5 | 90.9% | 1836.2 | 10022.1 | 0.545 |
| 8 | 1.876 | kimi-k2.6 | 93.1% | 2057.9 | 2753.2 | 0.486 |
| 9 | 1.642 | claude-opus-4.7 | 92.9% | 2323.2 | 4294.0 | 0.430 |
| 10 | 0.921 | glm-5.1-fw | 91.4% | 3841.4 | 10775.0 | 0.260 |
| 11 | 0.300 | minimax-m2.7 | 86.9% | 9771.5 | 23490.3 | 0.102 |
| 12 | 0.184 | qwen3.5-flash | 89.0% | 17337.1 | 36911.3 | 0.058 |

[^accuracy]: Output accuracy = (direction accuracy + Macro F1) / 2. MAE is kept for audit but excluded from the public score.

[^score]: Score = `QPS * [-log2(1 - output_accuracy + 0.0001)]`.

[^latency]: News latency is single-news end-to-end latency under no batching and no response caching. It can still be affected by network jitter, provider routing, hardware load, and runtime configuration.

[^coi]: `newsliquid-1.0-flash` is an in-house specialist developed by the benchmark organiser and tuned for low-latency single-news triage. Its score should be read with this conflict of interest in mind; sorting by raw output accuracy is a useful robustness check.

## Reading The Table

This is an information-rate leaderboard, not a pure accuracy leaderboard. It is designed for financial-news systems that must trade off timeliness and correctness under a consistent test environment.

`newsliquid-1.0-flash` ranks first because it is much faster, while its output accuracy remains below the strongest general-purpose frontier models. This is a deliberate low-latency tradeoff and an in-house submission from the benchmark organiser; for weakly time-sensitive or high-stakes review, use a stronger model or a human analyst as a second pass.

## Result Files

`results/leaderboard.json` includes a copy of the benchmark metadata as a release snapshot so a result file remains self-describing if copied outside the package. The canonical metadata file is `data/metadata.json`.

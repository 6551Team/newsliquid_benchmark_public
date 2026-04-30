# Annotation Guide

## Annotation Status

The labels in `data/reference_labels.jsonl` are human-annotated benchmark test-set labels. They are the official scoring reference for this release.

## Core Question

For the target asset, does this news item create a clear bullish, bearish, or neutral market-impact signal?

## Direction

- `long`: direct positive catalyst for demand, liquidity, legitimacy, adoption, supply reduction, or risk relief.
- `short`: direct negative catalyst such as delisting, exploit, legal pressure, insolvency, unlock overhang, or demand loss.
- `neutral`: weak link to the target asset, mostly macro background, mixed implications, or no clear tradable signal.

## Impact Score

- 0-10: almost no direct asset impact.
- 20-40: weak or indirect impact.
- 50-70: meaningful asset-level catalyst.
- 80-100: major, direct catalyst with strong likely market attention.

## Reason Style

Write one concise analyst note. Avoid model-like templates, avoid future price claims, and do not use realized K-line movement.

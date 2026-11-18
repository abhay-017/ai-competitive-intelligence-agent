# Evaluation plan

## Why
An LLM classifier is only useful if its categories and impact scores match what a human analyst would decide. This plan measures that honestly, including failures.

## Building the evaluation set
1. Let Workflow A run for 1–2 weeks (or run it manually several times) until `Intel_Log` has 40 or more rows.
2. Export `Intel_Log` as CSV and copy 40 rows into `evaluation/eval_set.csv` (template: `evaluation/eval_set_template.csv`). Pick a mix: about 10 per main category, plus some noise.
3. **Before looking at the model's answer**, fill in `human_category` and `human_impact` (1–10) for each row. Write a short note when unsure.
4. Run the scorer:

```bash
python evaluation/score_eval.py evaluation/eval_set.csv
```

## Metrics reported
| Metric | Formula |
|---|---|
| Category accuracy | matches / total |
| Per-category precision and recall | standard; shows which categories get confused |
| Impact MAE | mean absolute error between model and human impact |
| Alert precision | items with model ≥ 7 that the human also scored ≥ 7, out of all items with model ≥ 7 |
| High-impact recall | items with human ≥ 7 that the model also scored ≥ 7, out of all items with human ≥ 7 |
| Relevance accuracy | the model's `is_relevant` vs a human check |

## Failure modes to look for (and report)
- **Generic names**: "Linear regression" or "notion of…" articles matched as competitors.
- **Listicles** ("Top 10 Jira alternatives") over-scored.
- **campaign vs product_launch** confusion when a launch is announced at an event.
- **Headline-only items** (short Google News snippets) give lower confidence.
- **Same story from many outlets** (partly handled by title deduplication).

## Results
Fill this table after your run. Do not invent numbers.

| Metric | Result | Notes |
|---|---|---|
| Category accuracy | | |
| Impact MAE | | |
| Alert precision | | |
| High-impact recall | | |
| Biggest failure | | |
| Fix tried | | |

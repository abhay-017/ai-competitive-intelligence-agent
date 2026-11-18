"""Scores the classifier against human labels.

Usage: python score_eval.py eval_set.csv
CSV columns: model_category, model_impact, human_category, human_impact
(optional: model_is_relevant, human_is_relevant)
"""
import csv
import sys
from collections import Counter

THRESHOLD = 7

def main(path):
    rows = [r for r in csv.DictReader(open(path, encoding="utf-8")) if r.get("human_category")]
    if not rows:
        sys.exit("No labelled rows found (fill human_category / human_impact).")

    n = len(rows)
    correct = sum(r["model_category"].strip() == r["human_category"].strip() for r in rows)
    mae = sum(abs(float(r["model_impact"]) - float(r["human_impact"])) for r in rows) / n

    model_hi = [r for r in rows if float(r["model_impact"]) >= THRESHOLD]
    human_hi = [r for r in rows if float(r["human_impact"]) >= THRESHOLD]
    both_hi = [r for r in model_hi if float(r["human_impact"]) >= THRESHOLD]

    print(f"Items evaluated        : {n}")
    print(f"Category accuracy      : {correct / n:.0%} ({correct}/{n})")
    print(f"Impact MAE             : {mae:.2f}")
    print(f"Alert precision (>= {THRESHOLD}) : "
          + (f"{len(both_hi) / len(model_hi):.0%} ({len(both_hi)}/{len(model_hi)})" if model_hi else "n/a (no alerts)"))
    print(f"High-impact recall     : "
          + (f"{len(both_hi) / len(human_hi):.0%} ({len(both_hi)}/{len(human_hi)})" if human_hi else "n/a"))

    if all(r.get("human_is_relevant") for r in rows):
        rel = sum(r["model_is_relevant"].strip().lower() == r["human_is_relevant"].strip().lower() for r in rows)
        print(f"Relevance accuracy     : {rel / n:.0%}")

    print("\nPer-category precision / recall:")
    cats = sorted({r["human_category"] for r in rows} | {r["model_category"] for r in rows})
    for c in cats:
        tp = sum(r["model_category"] == c and r["human_category"] == c for r in rows)
        p = sum(r["model_category"] == c for r in rows)
        h = sum(r["human_category"] == c for r in rows)
        print(f"  {c:15s} precision {tp / p if p else 0:.0%}  recall {tp / h if h else 0:.0%}  (n={h})")

    confusions = Counter((r["human_category"], r["model_category"]) for r in rows
                         if r["human_category"] != r["model_category"])
    if confusions:
        print("\nMost common confusions (human -> model):")
        for (h, m), k in confusions.most_common(5):
            print(f"  {h} -> {m}: {k}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "eval_set.csv")

#!/usr/bin/env python3
import argparse
import os
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()

df = pd.read_csv(args.input, sep="\t")
if df.empty:
    out = pd.DataFrame(columns=["family","n_samples","n_candidates","mean_novelty_score","max_novelty_score"])
else:
    out = df.groupby("family").agg(
        n_samples=("sample_id", "nunique"),
        n_candidates=("region_id", "count"),
        mean_novelty_score=("novelty_score", "mean"),
        max_novelty_score=("novelty_score", "max")
    ).reset_index().sort_values("max_novelty_score", ascending=False)

os.makedirs(os.path.dirname(args.out), exist_ok=True)
out.to_csv(args.out, sep="\t", index=False)

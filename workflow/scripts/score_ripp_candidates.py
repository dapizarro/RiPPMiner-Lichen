#!/usr/bin/env python3
import argparse
import os
import numpy as np
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--ranked", required=True)
    ap.add_argument("--scores", required=True)
    args = ap.parse_args()

    df = pd.read_csv(args.input, sep="\t")
    if df.empty:
        os.makedirs(os.path.dirname(args.ranked), exist_ok=True)
        df.to_csv(args.ranked, sep="\t", index=False)
        df.to_csv(args.scores, sep="\t", index=False)
        return

    fam_counts = df.groupby("family")["region_id"].transform("count")
    sample_counts = df.groupby("sample_id")["region_id"].transform("count")
    rarity = 1 / fam_counts.clip(lower=1)

    df["rarity_score"] = rarity
    df["tailoring_score"] = np.log1p(df["tailoring_gene_count"])
    df["precursor_score"] = np.log1p(df["short_precursor_like_cds"])
    df["compactness_score"] = 1 / np.sqrt(df["gene_count"].clip(lower=1))
    df["unknown_score"] = df["cluster_type_raw"].fillna("").str.contains("unknown|other", case=False, regex=True).astype(int)

    df["novelty_score"] = (
        3.0 * df["is_ripp_annotated"] +
        0.7 * df["tailoring_score"] +
        1.5 * df["precursor_score"] +
        2.0 * df["rarity_score"] +
        1.0 * df["unknown_score"] +
        0.5 * df["compactness_score"]
    )
    df["priority_rank"] = df["novelty_score"].rank(ascending=False, method="first").astype(int)
    df = df.sort_values(["novelty_score", "tailoring_gene_count"], ascending=[False, False])

    os.makedirs(os.path.dirname(args.ranked), exist_ok=True)
    df.to_csv(args.ranked, sep="\t", index=False)
    df[["sample_id","species","family","region_id","novelty_score","priority_rank","candidate_reason"]].to_csv(args.scores, sep="\t", index=False)

if __name__ == "__main__":
    main()

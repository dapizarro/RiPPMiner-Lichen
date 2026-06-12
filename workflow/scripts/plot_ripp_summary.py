#!/usr/bin/env python3
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("--ranked", required=True)
ap.add_argument("--family", required=True)
ap.add_argument("--per-sample", required=True)
ap.add_argument("--by-family", required=True)
ap.add_argument("--novelty", required=True)
args = ap.parse_args()

os.makedirs(os.path.dirname(args.per_sample), exist_ok=True)
df = pd.read_csv(args.ranked, sep="\t")
fam = pd.read_csv(args.family, sep="\t")

# Plot 1
plt.figure(figsize=(8, 4))
if not df.empty:
    counts = df.groupby("sample_id").size().sort_values(ascending=False)
    counts.plot(kind="bar")
plt.ylabel("RiPP-like candidate BGCs")
plt.xlabel("Sample")
plt.tight_layout()
plt.savefig(args.per_sample)
plt.close()

# Plot 2
plt.figure(figsize=(8, 4))
if not fam.empty:
    fam.set_index("family")["n_candidates"].sort_values(ascending=False).plot(kind="bar")
plt.ylabel("RiPP-like candidate BGCs")
plt.xlabel("Family")
plt.tight_layout()
plt.savefig(args.by_family)
plt.close()

# Plot 3
plt.figure(figsize=(8, 4))
if not df.empty:
    top = df.sort_values("novelty_score", ascending=False).head(20)
    labels = top["sample_id"].astype(str) + ":" + top["region_id"].astype(str)
    plt.barh(labels[::-1], top["novelty_score"][::-1])
plt.xlabel("Novelty / priority score")
plt.ylabel("Candidate")
plt.tight_layout()
plt.savefig(args.novelty)
plt.close()

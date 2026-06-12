#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import pandas as pd
from Bio import SeqIO


def contains_any(text, keywords):
    text = text.lower()
    return any(k.lower() in text for k in keywords)


def feature_text(feature):
    vals = []
    for key, value in feature.qualifiers.items():
        if isinstance(value, list):
            vals.extend([str(v) for v in value])
        else:
            vals.append(str(value))
    return " ".join(vals)


def parse_gbk(gbk, sample_id, ripp_keywords, tailoring_keywords):
    rows = []
    for rec in SeqIO.parse(str(gbk), "genbank"):
        product_texts = []
        gene_count = 0
        tailoring_count = 0
        short_precursors = 0
        candidate_reason = []
        cluster_type = "unknown"

        for feat in rec.features:
            txt = feature_text(feat)
            if feat.type in {"protocluster", "cand_cluster", "region"}:
                product_texts.append(txt)
                if contains_any(txt, ripp_keywords):
                    candidate_reason.append("antiSMASH_RiPP_annotation")
                    cluster_type = txt[:120]
            if feat.type == "CDS":
                gene_count += 1
                if contains_any(txt, tailoring_keywords):
                    tailoring_count += 1
                trans = feat.qualifiers.get("translation", [""])[0]
                if trans and len(trans) <= 120:
                    short_precursors += 1

        all_text = " ".join(product_texts)
        is_ripp = contains_any(all_text, ripp_keywords)
        has_precursor_signal = short_precursors > 0 and tailoring_count > 0
        if has_precursor_signal:
            candidate_reason.append("short_precursor_like_CDS_plus_tailoring")
        if is_ripp or has_precursor_signal:
            rows.append({
                "sample_id": sample_id,
                "gbk_file": str(gbk),
                "region_id": rec.id,
                "cluster_type_raw": cluster_type if cluster_type != "unknown" else all_text[:120],
                "is_ripp_annotated": int(is_ripp),
                "gene_count": gene_count,
                "tailoring_gene_count": tailoring_count,
                "short_precursor_like_cds": short_precursors,
                "candidate_reason": ";".join(sorted(set(candidate_reason))) or "RiPP_keyword"
            })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--antismash-dir", required=True)
    ap.add_argument("--metadata", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ripp-keywords", required=True)
    ap.add_argument("--tailoring-keywords", required=True)
    args = ap.parse_args()

    ripp_keywords = [x.strip() for x in args.ripp_keywords.split(",") if x.strip()]
    tailoring_keywords = [x.strip() for x in args.tailoring_keywords.split(",") if x.strip()]
    meta = pd.read_csv(args.metadata, sep="\t")
    all_rows = []

    base = Path(args.antismash_dir)
    for sample_id in meta["sample_id"].astype(str):
        sample_dir = base / sample_id
        gbks = sorted(sample_dir.glob("*.gbk")) + sorted(sample_dir.glob("*.gbff"))
        for gbk in gbks:
            all_rows.extend(parse_gbk(gbk, sample_id, ripp_keywords, tailoring_keywords))

    df = pd.DataFrame(all_rows)
    if df.empty:
        df = pd.DataFrame(columns=["sample_id","gbk_file","region_id","cluster_type_raw","is_ripp_annotated","gene_count","tailoring_gene_count","short_precursor_like_cds","candidate_reason"])
    df = df.merge(meta, on="sample_id", how="left")
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    df.to_csv(args.out, sep="\t", index=False)

if __name__ == "__main__":
    main()

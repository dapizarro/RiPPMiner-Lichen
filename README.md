# RiPPMiner-Lichen

**RiPPMiner-Lichen** is a reproducible workflow for detecting, summarising and prioritising putative RiPP-like biosynthetic gene clusters in lichen-forming fungi from antiSMASH outputs.

This repository is designed as a lightweight, reusable companion workflow for lichen biosynthetic genomics. It does **not** reproduce any single published study directly; instead, it provides a general framework to explore RiPP candidates in non-model fungal genomes.

## Why RiPPs in lichens?

Recent paired-omics and comparative genomics work on lichenized fungi suggests that RiPP-related biosynthetic gene clusters may represent an unexpectedly important and underexplored fraction of the lichen biosynthetic landscape. RiPPMiner-Lichen focuses on this neglected class and helps identify candidate clusters for downstream comparative genomics, phylogenetic profiling, metabolomics integration, or heterologous-expression prioritisation.

## Main features

- Parse antiSMASH GenBank outputs.
- Detect candidate RiPP / RiPP-like clusters.
- Extract cluster-level features.
- Estimate taxonomic rarity.
- Score candidate novelty.
- Rank RiPP-like BGCs for follow-up.
- Generate summary tables and publication-style plots.
- Run with or without metabolomics data.

## Repository structure

```text
RiPPMiner-Lichen/
├── README.md
├── LICENSE
├── CITATION.cff
├── Snakefile
├── config/
│   └── config.yaml
├── data/
│   ├── metadata.tsv
│   └── example_antismash/
├── workflow/
│   └── scripts/
├── envs/
│   └── rippminer.yaml
├── results/
├── docs/
└── tests/
```

## Quick start

```bash
git clone https://github.com/dapizarro/RiPPMiner-Lichen.git
cd RiPPMiner-Lichen
mamba env create -f envs/rippminer.yaml
mamba activate rippminer
snakemake --cores 4
```

The example dataset included in `data/example_antismash/` is artificial and only intended to test the workflow.

## Input files

### 1. antiSMASH output folders

Place one antiSMASH output folder per genome/sample in:

```text
data/antismash/
```

Each folder should contain GenBank files such as:

```text
sample_01.region001.gbk
sample_01.region002.gbk
```

For testing, the workflow uses:

```text
data/example_antismash/
```

### 2. Metadata table

Required file:

```text
data/metadata.tsv
```

Minimum columns:

```text
sample_id	species	genus	family
```

Optional columns:

```text
chemotype	habitat	country	voucher
```

## Output files

```text
results/ripp_candidates.tsv
results/ripp_ranked_candidates.tsv
results/ripp_family_summary.tsv
results/ripp_novelty_scores.tsv
results/figures/ripp_candidates_per_sample.pdf
results/figures/ripp_candidates_by_family.pdf
results/figures/ripp_novelty_ranking.pdf
```

## Candidate scoring

The default novelty score combines:

- RiPP-like product annotation.
- Presence of tailoring enzymes.
- Cluster size.
- Taxonomic rarity.
- Lack of similarity annotation.
- Presence of short precursor-like peptides.

This is a prioritisation score, not experimental validation.

## Typical use case

```bash
# Edit config/config.yaml
snakemake --cores 8
```

Then inspect:

```text
results/ripp_ranked_candidates.tsv
```

The highest-ranking candidates are good targets for:

- manual antiSMASH inspection,
- BiG-SCAPE / BiG-SLiCE clustering,
- comparison with MIBiG,
- metabolomics-guided deorphanisation,
- expression or co-expression analysis,
- targeted MS/MS validation.

## Citation

If you use this workflow, cite the repository DOI once archived in Zenodo and cite the relevant antiSMASH, BiG-SCAPE, MIBiG and lichen biosynthetic genomics literature.

## Authorship note

This repository is intended as a general methodological workflow for RiPP candidate prioritisation in lichen-forming fungi. It is conceptually inspired by recent comparative lichen biosynthetic genomics, but it is not a reimplementation of any individual study.

# RiPPMiner-Lichen

![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20700515.svg) (https://doi.org/10.5281/zenodo.20700515)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

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

---

## Scientific Background

RiPPMiner-Lichen was developed within ongoing research on biosynthetic diversity and natural product discovery in lichen-forming fungi.

The workflow is conceptually informed by recent comparative genomics and paired-omics studies exploring biosynthetic gene clusters across lichenized fungi, including:

> Singh G., Xu M., Zdouc M., Pasinato A., Egbert S., Yu X., Pizarro D., et al. (2025). Paired-omics-based exploration and characterization of biosynthetic diversity in lichenized fungi. Microbial Genomics.

> Singh G., Pasinato A., Yriarte A.L.C., Pizarro D., et al. (2024). Are there conserved biosynthetic genes in lichens? Genome-wide assessment of terpene biosynthetic genes suggests conserved evolution of the squalene synthase cluster.

RiPPMiner-Lichen is not a reimplementation of any individual study. Instead, it provides a reusable framework for identifying and prioritizing RiPP-like biosynthetic loci across fungal genomes.

## Citation

If you use this workflow, cite the repository as Pizarro, D. (2026). RiPPMiner-Lichen: prioritisation of RiPP-like biosynthetic gene clusters in lichen-forming fungi (v1.0). Zenodo. https://doi.org/10.5281/zenodo.20700515 and cite the relevant antiSMASH, BiG-SCAPE, MIBiG and lichen biosynthetic genomics literature.

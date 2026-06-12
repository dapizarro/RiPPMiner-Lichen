configfile: "config/config.yaml"

RESULTS = config["results_dir"]

rule all:
    input:
        f"{RESULTS}/ripp_candidates.tsv",
        f"{RESULTS}/ripp_ranked_candidates.tsv",
        f"{RESULTS}/ripp_family_summary.tsv",
        f"{RESULTS}/figures/ripp_candidates_per_sample.pdf",
        f"{RESULTS}/figures/ripp_candidates_by_family.pdf",
        f"{RESULTS}/figures/ripp_novelty_ranking.pdf"

rule parse_antismash:
    input:
        metadata=config["metadata"]
    output:
        f"{RESULTS}/ripp_candidates.tsv"
    params:
        antismash_dir=config["antismash_dir"],
        ripp_keywords=",".join(config["ripp_keywords"]),
        tailoring_keywords=",".join(config["tailoring_keywords"])
    shell:
        "python workflow/scripts/parse_antismash_ripps.py --antismash-dir {params.antismash_dir} --metadata {input.metadata} --out {output} --ripp-keywords '{params.ripp_keywords}' --tailoring-keywords '{params.tailoring_keywords}'"

rule score_candidates:
    input:
        f"{RESULTS}/ripp_candidates.tsv"
    output:
        ranked=f"{RESULTS}/ripp_ranked_candidates.tsv",
        scores=f"{RESULTS}/ripp_novelty_scores.tsv"
    shell:
        "python workflow/scripts/score_ripp_candidates.py --input {input} --ranked {output.ranked} --scores {output.scores}"

rule summarize_by_family:
    input:
        f"{RESULTS}/ripp_ranked_candidates.tsv"
    output:
        f"{RESULTS}/ripp_family_summary.tsv"
    shell:
        "python workflow/scripts/summarize_by_family.py --input {input} --out {output}"

rule plot_results:
    input:
        ranked=f"{RESULTS}/ripp_ranked_candidates.tsv",
        family=f"{RESULTS}/ripp_family_summary.tsv"
    output:
        per_sample=f"{RESULTS}/figures/ripp_candidates_per_sample.pdf",
        by_family=f"{RESULTS}/figures/ripp_candidates_by_family.pdf",
        novelty=f"{RESULTS}/figures/ripp_novelty_ranking.pdf"
    shell:
        "python workflow/scripts/plot_ripp_summary.py --ranked {input.ranked} --family {input.family} --per-sample {output.per_sample} --by-family {output.by_family} --novelty {output.novelty}"

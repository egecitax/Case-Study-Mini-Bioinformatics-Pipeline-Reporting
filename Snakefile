configfile: "config/config.yaml"

SAMPLE  = config["sample"]
FASTQ   = config["fastq"]
OUTDIR  = config.get("outdir", "results")
THREADS = int(config.get("threads", 4))

rule all:
    input:
        f"{OUTDIR}/nanoplot/{SAMPLE}/NanoPlot-report.html",
        f"{OUTDIR}/stats/{SAMPLE}.read_stats.csv",
        f"{OUTDIR}/plots/{SAMPLE}.summary.txt",
        f"{OUTDIR}/plots/{SAMPLE}.gc_content_hist.png",
        f"{OUTDIR}/plots/{SAMPLE}.read_length_hist.png",
        f"{OUTDIR}/plots/{SAMPLE}.mean_q_hist.png"

rule nanoplot_qc:
    conda: "envs/longread_qc.yml"
    input:
        fastq=FASTQ
    output:
        html=f"{OUTDIR}/nanoplot/{SAMPLE}/NanoPlot-report.html"
    threads: THREADS
    shell:
        r"""
        mkdir -p {OUTDIR}/nanoplot/{SAMPLE}
        NanoPlot --fastq {input.fastq} \
                 --outdir {OUTDIR}/nanoplot/{SAMPLE} \
                 --threads {threads} \
                 --loglength
        """

rule compute_read_stats:
    conda: "envs/longread_qc.yml"
    input:
        fastq=FASTQ
    output:
        csv=f"{OUTDIR}/stats/{SAMPLE}.read_stats.csv"
    shell:
        r"""
        mkdir -p {OUTDIR}/stats
        python scripts/compute_read_stats.py \
            --fastq {input.fastq} \
            --out {output.csv}
        """

rule plot_distributions:
    conda: "envs/longread_qc.yml"
    input:
        csv=f"{OUTDIR}/stats/{SAMPLE}.read_stats.csv"
    output:
        summary=f"{OUTDIR}/plots/{SAMPLE}.summary.txt",
        gc=f"{OUTDIR}/plots/{SAMPLE}.gc_content_hist.png",
        length=f"{OUTDIR}/plots/{SAMPLE}.read_length_hist.png",
        meanq=f"{OUTDIR}/plots/{SAMPLE}.mean_q_hist.png"
    shell:
        r"""
        mkdir -p {OUTDIR}/plots
        python scripts/plot_distributions.py \
            --csv {input.csv} \
            --out-summary {output.summary} \
            --out-gc {output.gc} \
            --out-length {output.length} \
            --out-meanq {output.meanq}
        """
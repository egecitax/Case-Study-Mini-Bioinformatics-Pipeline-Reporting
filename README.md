# Mini Bioinformatics Pipeline – Long-Read QC Analysis

This repository contains a **reproducible bioinformatics pipeline** for performing quality control and exploratory analysis of long-read sequencing data.
The workflow is implemented using **Snakemake** and runs inside a **Docker container**, ensuring that the analysis can be reproduced consistently across different environments.

The pipeline performs automated **quality control, read statistics calculation, and data visualization** on a FASTQ sequencing dataset.

---

# Objective

The goal of this project is to create a reproducible pipeline that:

1. Performs **quality control (QC)** on raw long-read sequencing data.
2. Calculates read-level statistics.
3. Generates visualizations and summary statistics to help researchers understand the characteristics of the dataset before downstream analysis.

---

# Pipeline Overview

The pipeline consists of three main stages.

### 1. Quality Control (QC)

The workflow uses **NanoPlot**, a QC tool designed specifically for **long-read sequencing technologies** such as Oxford Nanopore and PacBio.

NanoPlot generates an HTML report that summarizes sequencing read characteristics such as:

* read length distribution
* quality score distribution
* sequencing yield

---

### 2. Read Statistics Calculation

A custom Python script processes each read in the FASTQ file and calculates:

* **GC content (%)**
* **Read length (bp)**
* **Mean read quality score (Phred)**

These values are saved in a structured CSV file:

```
results/stats/run1.read_stats.csv
```

---

### 3. Data Visualization

A separate visualization script generates plots showing the distributions of:

* GC content
* Read lengths
* Mean read quality scores

Output files:

```
results/plots/run1.gc_content_hist.png
results/plots/run1.read_length_hist.png
results/plots/run1.mean_q_hist.png
```

The script also computes summary statistics (mean, median, min, max) for each metric and saves them to:

```
results/plots/run1.summary.txt
```

---

# Example Results

The pipeline was executed on the provided dataset (`barcode77.fastq.gz`).

Key summary statistics:

Total reads: **81,011**

GC Content
Mean: **53.0%**
Median: **53.5%**

Read Length
Mean: **1038 bp**
Median: **547 bp**
Maximum: **686,155 bp**

Mean Read Quality
Mean: **Q17.9**
Median: **Q17.3**

---

## Interpretation

**GC Content**

The GC content distribution is centered around ~53% and shows a relatively smooth, unimodal distribution.
This suggests that the dataset does not exhibit strong GC bias or obvious contamination.

**Read Length**

The read length distribution shows a large number of shorter reads and a smaller number of extremely long reads.
This long-tailed pattern is typical for long-read sequencing technologies.

**Read Quality**

The mean read quality is approximately Q18.
For long-read sequencing platforms such as Nanopore, this quality level is generally considered sufficient for downstream analyses such as alignment.

Overall, the dataset appears suitable for further analysis.

---

# Repository Structure

```
.
├── Snakefile
├── Dockerfile
├── README.md
├── EMAIL_TO_PROFESSOR.md
├── config
│   └── config.yaml
├── envs
│   └── longread_qc.yml
├── scripts
│   ├── compute_read_stats.py
│   └── plot_distributions.py
└── data
```

---

# Running the Pipeline

The pipeline runs inside Docker to ensure reproducibility.

### Build Docker image

```
docker build -t longread-qc .
```

### Run the pipeline

```
docker run --rm -it -v ${PWD}:/work longread-qc snakemake --cores 4
```

This will automatically execute all pipeline steps and generate the QC report, statistics, and visualizations.

---

# Reproducibility

The workflow is reproducible because:

* it is defined using **Snakemake**
* all dependencies are included inside a **Docker container**
* the pipeline can be executed with a single command

This ensures that the analysis can be reproduced consistently across different systems.

---

# Communication

A sample communication summarizing the results for a non-technical collaborator is included in:

```
EMAIL_TO_PROFESSOR.md
```

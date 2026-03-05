# Mini Bioinformatics Pipeline – Long-Read QC & Reporting

## Overview

This repository contains a **reproducible bioinformatics pipeline** that performs **quality control and exploratory analysis of long-read sequencing data** from FASTQ files.

The pipeline was designed as a minimal but realistic workflow to help researchers quickly understand the quality characteristics of sequencing reads before performing computationally expensive downstream analyses such as alignment or assembly.

The workflow is implemented using **Snakemake** and executed inside a **Docker container**, ensuring that the analysis is fully reproducible and easy to run on any machine.

Workflow managers like Snakemake are widely used in bioinformatics to automate multi-step analyses and make them reproducible by defining rules that transform input files into outputs through chained steps. ([carpentries-incubator.github.io][1])

---

# Pipeline Functionality

The pipeline performs the following steps automatically:

### 1. Long-Read Quality Control

The workflow runs **NanoPlot**, a tool designed specifically for analyzing long-read sequencing data and generating visual summaries of read quality and length distributions. ([Front Line Genomics][2])

NanoPlot generates an HTML report containing plots and summary statistics describing the dataset.

---

### 2. Custom Read-Level Statistics

A Python script processes the FASTQ file and computes key statistics for **each individual read**:

* GC content (%)
* Read length
* Mean Phred quality score

These statistics are saved in a structured format:

```
results/stats/run1.read_stats.csv
```

---

### 3. Visualization

Another Python script automatically generates distribution plots showing:

* GC content distribution
* Read length distribution
* Mean read quality distribution

These plots help researchers quickly assess whether the sequencing run produced data suitable for downstream analysis.

---

### 4. Summary Statistics

The pipeline also generates a summary report containing key metrics such as:

* Mean
* Median
* Minimum
* Maximum

for each computed statistic.

Example output file:

```
results/plots/run1.summary.txt
```

---

# Workflow Structure

```
FASTQ input
     ↓
NanoPlot QC
     ↓
Custom read statistics (Python)
     ↓
CSV output
     ↓
Visualization generation
     ↓
Summary statistics
```

---

# Project Structure

```
Case-Study-Mini-Bioinformatics-Pipeline-Reporting
│
├── Snakefile
├── Dockerfile
├── .gitignore
│
├── config
│   └── config.yaml
│
├── envs
│   └── longread_qc.yml
│
├── scripts
│   ├── compute_read_stats.py
│   └── plot_distributions.py
│
├── data
│   └── demo.fastq
```

---

# Requirements

The pipeline requires only:

* **Docker Desktop**

All dependencies are automatically installed inside the container.

---

# Running the Pipeline

### 1. Clone the repository

```bash
git clone https://github.com/egecitax/Case-Study-Mini-Bioinformatics-Pipeline-Reporting.git
cd Case-Study-Mini-Bioinformatics-Pipeline-Reporting
```

---

### 2. Build the Docker image

```bash
docker build -t longread-qc .
```

---

### 3. Run the pipeline

```bash
docker run --rm -it -v ${PWD}:/work longread-qc snakemake --cores 4
```

The pipeline will automatically generate results inside the `results/` directory.

---

# Output Files

After execution, the pipeline produces:

```
results/
│
├── nanoplot/
│   └── run1/
│       └── NanoPlot-report.html
│
├── stats/
│   └── run1.read_stats.csv
│
└── plots/
    ├── run1.gc_content_hist.png
    ├── run1.read_length_hist.png
    ├── run1.mean_q_hist.png
    └── run1.summary.txt
```

### Output Description

| Output              | Description                                         |
| ------------------- | --------------------------------------------------- |
| NanoPlot report     | Interactive QC report for long-read sequencing data |
| Read statistics CSV | Per-read computed statistics                        |
| Distribution plots  | Visual summaries of GC, length, and quality         |
| Summary report      | Mean/median/min/max statistics                      |

---

# Using Your Own FASTQ File

Replace the FASTQ file inside the `data/` directory.

Example:

```
data/input.fastq.gz
```

Then update the configuration file:

```
config/config.yaml
```

Example:

```
fastq: "data/input.fastq.gz"
```

Run the pipeline again with the same Docker command.

---

# Notes

The repository includes a small **demo FASTQ file** to demonstrate pipeline functionality.

For real sequencing runs, users should provide their own FASTQ datasets.

---

# Technologies Used

* Snakemake
* Docker
* Python
* Biopython
* Pandas
* Matplotlib
* NanoPlot

---

# Author

**Ege Çıtak**
Artificial Intelligence & Data Engineering
Ankara University

[1]: https://carpentries-incubator.github.io/snakemake-novice-bioinformatics/?utm_source=chatgpt.com "Snakemake for Bioinformatics: Summary and Setup"
[2]: https://frontlinegenomics.com/how-to-ngs-quality-control/?utm_source=chatgpt.com "How-to: NGS Quality Control"

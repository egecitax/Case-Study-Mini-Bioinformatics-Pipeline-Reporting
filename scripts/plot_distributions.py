#!/usr/bin/env python3
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def write_summary(df: pd.DataFrame, out_path: str):
    metrics = {
        "gc_percent": "GC Content (%)",
        "read_length": "Read Length (bp)",
        "mean_q": "Mean Read Quality (Phred)",
    }

    lines = []
    lines.append(f"n_reads\t{len(df)}")

    for col, label in metrics.items():
        series = df[col].dropna()
        lines.append(f"\n[{label}]")
        lines.append(f"mean\t{series.mean():.4f}")
        lines.append(f"median\t{series.median():.4f}")
        lines.append(f"min\t{series.min():.4f}")
        lines.append(f"max\t{series.max():.4f}")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def hist(series, title, xlabel, out_png, bins=60):
    plt.figure()
    plt.hist(series.dropna(), bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out-summary", required=True)
    ap.add_argument("--out-gc", required=True)
    ap.add_argument("--out-length", required=True)
    ap.add_argument("--out-meanq", required=True)
    args = ap.parse_args()

    df = pd.read_csv(args.csv)

    write_summary(df, args.out_summary)

    hist(df["gc_percent"], "GC Content Distribution", "GC (%)", args.out_gc)
    hist(df["read_length"], "Read Length Distribution", "Length (bp)", args.out_length)
    hist(df["mean_q"], "Mean Read Quality Distribution", "Mean Q (Phred)", args.out_meanq)

if __name__ == "__main__":
    main()
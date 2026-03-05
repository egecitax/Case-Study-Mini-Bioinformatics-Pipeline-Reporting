#!/usr/bin/env python3
import argparse
import gzip
from Bio import SeqIO
import pandas as pd

def open_maybe_gz(path: str):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path, "rt")

def mean_phred(quals):
    # quals: list[int] already phred scores in Biopython
    return sum(quals) / len(quals) if quals else 0.0

def gc_percent(seq: str):
    if not seq:
        return 0.0
    s = seq.upper()
    gc = s.count("G") + s.count("C")
    return (gc / len(s)) * 100.0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fastq", required=True, help="Input FASTQ(.gz) long-read file")
    ap.add_argument("--out", required=True, help="Output CSV path")
    args = ap.parse_args()

    rows = []
    with open_maybe_gz(args.fastq) as handle:
        for rec in SeqIO.parse(handle, "fastq"):
            seq = str(rec.seq)
            quals = rec.letter_annotations.get("phred_quality", [])
            rows.append({
                "read_id": rec.id,
                "read_length": len(seq),
                "gc_percent": gc_percent(seq),
                "mean_q": mean_phred(quals),
            })

    df = pd.DataFrame(rows)
    df.to_csv(args.out, index=False)

if __name__ == "__main__":
    main()
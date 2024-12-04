#!/usr/bin/env python3
"""
Add a 'safe_id' column to a TSV file containing sequencing data.

The safe_id is constructed as '{IRIDA_ID}_{S_number}' where:
- IRIDA_ID comes from the 'IRIDA_ID' column
- S_number is extracted from the Raw_forward filepath using regex pattern 'S\d+'
  (e.g., from 'PID-0760-108s_S57_L001_R1_001.fastq.gz', extracts 'S57')

Usage:
    add_col.py [original_tsv] [new_tsv]

Arguments:
    original_tsv: Path to input TSV file
    new_tsv: Path where the modified TSV will be saved

Example output safe_id:
    For IRIDA_ID=1081 and Raw_forward containing 'S57': '1081_S57'
"""
import sys
import os
import re
import pandas as pd

def extract_s_number(filepath):
    basename = os.path.basename(filepath)
    match = re.search(r'S\d+', basename)
    return match.group() if match else None

def main():
    if len(sys.argv) != 3:
        print("Usage: add_col.py [original_tsv] [new_tsv]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Read TSV with tab separator
    df = pd.read_csv(input_file, sep='\t')

    # Create safe_id column
    df['safe_id'] = df.apply(
        lambda row: f"{row['IRIDA_ID']}_{extract_s_number(row['Raw_forward'])}", 
        axis=1
    )

    # Write output TSV
    df.to_csv(output_file, sep='\t', index=False)

if __name__ == "__main__":
    main()

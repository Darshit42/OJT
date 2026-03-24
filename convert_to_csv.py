"""
Quick converter: LD2011_2014 - Copy.txt -> LD2011_2014_converted.csv

Converts the semicolon-separated, European-decimal-format TXT file
into a standard comma-separated CSV with dot decimals.

Usage:
    python convert_to_csv.py
"""

import pandas as pd
import os
import time

INPUT_FILE = 'LD2011_2014 - Copy.txt'
OUTPUT_FILE = 'LD2011_2014_converted.csv'

df = pd.read_csv(
    INPUT_FILE,
    sep=';',
    decimal=',',
    index_col=0,
    parse_dates=True
)

df.index.name = 'datetime'

df.to_csv(OUTPUT_FILE)
print('Done!')

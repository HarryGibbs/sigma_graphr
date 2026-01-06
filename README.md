# Σgraphr

Σgraphr converts one or more sequences in a single FAS/FASTA file into **cumulative (left-to-right) character running-sum CSVs**.

For each sequence, Σgraphr:
- detects the distinct characters present (e.g. nucleotides, amino acids, or other codes)
- calculates a running total (∑) across the sequence for each character
- outputs one CSV per sequence, where each column is the cumulative total for one character

These CSVs can be opened in Excel or Google Sheets and plotted as line charts. Characters that are evenly distributed rise smoothly; uneven distributions rise irregularly.

This script is also available online (no code required) at:
http://54.190.199.170/sigma_graphr/

## Output
- **Single sequence input** → one CSV file  
- **Multiple sequences input** → multiple CSV files (often bundled as a ZIP by the included web wrapper)

## Example plot
![Example Σgraphr plots](graphic.png)

## Notes
- Input is standard FAS/FASTA: a header line beginning with `>` followed by one or more lines of sequence characters.
- CSV columns represent cumulative totals across positions from left to right.

## Credits / reference
Σgraphr is based on the same general style of cumulative visualization used in SNAP (Synonymous Nonsynonymous Analysis Program) and related sequence-variation approaches.

---

## Download from GitHub

### Option A: Download ZIP (no Git needed)
1. On the GitHub repo page, click the green **Code** button
2. Click **Download ZIP**
3. Unzip it somewhere on your computer

You should end up with a folder containing `sigma_graphr.py` in the root of the repo.

### Option B: Clone with Git (for developers)
```bash
git clone https://github.com/HarryGibbs/sigma_graphr
cd sigma_graphr
```

## Requirements
You must have **Python 3** installed.

- Windows: install Python 3 from python.org (make sure “Add Python to PATH” is enabled if you want to run it from the command line)
- macOS/Linux: Python 3 is often already installed, otherwise install via your package manager

No `pip install` is required (this script uses only the Python standard library).

## Run locally

1. Put your input FAS/FASTA files in the `input` folder (next to `sigma_graphr.py`)
2. Run the script
3. Find results in the `output` folder

### Run by double-click (Windows)
If `.py` files are associated with Python on your system, you can double-click `sigma_graphr.py`.
(If nothing happens, use one of the command-line options below.)

### Run from Command Prompt / Terminal (recommended)
Open a terminal in the repo folder (the one containing `sigma_graphr.py`), then run:

**Windows (most common):**
```bash
py sigma_graphr.py
```

**Windows / macOS / Linux:**
```bash
python sigma_graphr.py
```

**macOS / Linux (if `python` points to Python 2):**
```bash
python3 sigma_graphr.py
```

## Where the output goes
- Place `.fas` / `.fasta` / `.fa` files into `./input/`
- Output will be written into `./output/`
- If an input file contains multiple sequences, the script will generate a ZIP for that file (containing one CSV per sequence)

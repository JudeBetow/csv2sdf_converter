# CSV to SDF Converter

Convert a CSV file containing SMILES strings into an SDF file using RDKit.

This is useful when you have tabular compound data and want to export molecules for docking, visualization, cheminformatics workflows, or tools that expect Structure Data Format (`.sdf`) files.

## Features

- Reads a CSV file with a SMILES column.
- Detects the SMILES column case-insensitively.
- Also accepts column names containing `smile`, such as `canonical_smiles` or `std_smiles`.
- Skips blank, missing, or invalid SMILES rows.
- Computes 2D coordinates for easier viewing in molecule viewers.
- Preserves all non-SMILES CSV columns as SDF molecule properties.

## Requirements

- Python 3.8+
- pandas
- RDKit

Recommended installation with conda:

```bash
conda install -c conda-forge rdkit pandas
```

## Input Format

The input must be a CSV file with one molecule per row and a SMILES column.

Example:

```csv
smiles,name,source_id
CCO,ethanol,CMPD001
c1ccccc1,benzene,CMPD002
```

Any columns other than the SMILES column are written into the SDF as molecule properties.

## Usage

```bash
python csv2sdf.py input.csv output.sdf
```

Example:

```bash
python csv2sdf.py reframe_std.csv reframe_std.sdf
```

## Output

The script writes an SDF file at the output path you provide.

Each valid molecule receives:

- A structure generated from the SMILES string.
- 2D coordinates when RDKit can compute them.
- A molecule title based on the CSV row index.
- SDF properties copied from the other CSV columns.

At the end, the script prints a short summary:

```text
Read 100 rows. Converted 97 molecules, skipped 3 rows.
```

## Error Handling

The script exits with an error if:

- The CSV is empty.
- No SMILES-like column can be found.
- The input file cannot be read.

Rows with invalid SMILES are skipped rather than stopping the full conversion.

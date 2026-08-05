#!/usr/bin/env python3
# csv_to_sdf.py - more robust csv -> sdf converter
# usage: python csv_to_sdf.py input.csv output.sdf

import sys
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem

def _find_smiles_column(df):
    # exact match first (case-insensitive), then substring match
    cols = list(df.columns)
    for c in cols:
        if str(c).strip().lower() == "smiles":
            return c
    for c in cols:
        if "smile" in str(c).strip().lower():
            return c
    return None

def csv_to_sdf(csv_file, sdf_file):
    # read everything as object to avoid numeric coercion
    df = pd.read_csv(csv_file, dtype=object)
    if df.empty:
        raise ValueError("Input CSV is empty")

    smiles_col = _find_smiles_column(df)
    if smiles_col is None:
        raise KeyError(
            "Could not find a 'smiles' column (case-insensitive). "
            f"Columns present: {', '.join(map(str, df.columns))}"
        )

    writer = Chem.SDWriter(sdf_file)
    converted = 0
    skipped = 0

    for idx, row in df.iterrows():
        raw = row[smiles_col]
        if pd.isna(raw):
            skipped += 1
            continue
        smiles = str(raw).strip()
        if not smiles:
            skipped += 1
            continue

        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            # optionally print a warning for the bad SMILES:
            # print(f"Warning: invalid SMILES at row {idx}: {smiles}")
            skipped += 1
            continue

        # compute 2D coords (useful for many viewers)
        try:
            AllChem.Compute2DCoords(mol)
        except Exception:
            # if RDKit crashes on coords, proceed without coords
            pass

        # give the molecule a title (optional)
        try:
            mol.SetProp("_Name", str(idx))
        except Exception:
            pass

        # add other columns as properties, skip NaNs
        for col in df.columns:
            if col == smiles_col:
                continue
            val = row[col]
            if pd.isna(val):
                continue
            # convert to string
            try:
                mol.SetProp(str(col), str(val))
            except Exception:
                # skip properties that can't be set for some reason
                pass

        writer.write(mol)
        converted += 1

    writer.close()
    print(f"Read {len(df)} rows. Converted {converted} molecules, skipped {skipped} rows.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_sdf.py <input_csv_file> <output_sdf_file>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_sdf = sys.argv[2]

    try:
        csv_to_sdf(input_csv, output_sdf)
    except Exception as e:
        print("Error:", e)
        sys.exit(2)

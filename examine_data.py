import pandas as pd
import numpy as np

# Read the Excel file
excel_path = '/Users/jiangzixi/Downloads/出图/CMA- analysis.xlsx'
xl = pd.ExcelFile(excel_path)
df = xl.parse('Sheet1')

# Print the entire dataframe to understand its structure
print("Full DataFrame (first 20 rows):")
print(df.head(20))
print("\nFull DataFrame (last 20 rows):")
print(df.tail(20))

# Check for empty rows that might separate tables
empty_rows = df[df.isnull().all(axis=1)].index
print(f"\nEmpty rows at indices: {list(empty_rows)}")

# Check for potential table headers (rows with non-null values in the first column)
potential_headers = df[df[1].notnull()].index
print(f"\nPotential table headers at indices: {list(potential_headers)}")

# Examine what's in these header rows
print("\nContent of potential header rows:")
for idx in potential_headers:
    print(f"Row {idx}: {df.iloc[idx, 0]}")
    print(f"  Columns: {list(df.columns[df.iloc[idx].notnull()])}")
    print(f"  Values: {list(df.iloc[idx][df.iloc[idx].notnull()])}")
    print()
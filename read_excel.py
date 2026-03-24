import pandas as pd
import os

# Read the Excel file
excel_path = '/Users/jiangzixi/Downloads/出图/CMA- analysis.xlsx'

try:
    # Get all sheet names
    xl = pd.ExcelFile(excel_path)
    sheet_names = xl.sheet_names
    
    print(f"Found {len(sheet_names)} sheets in the Excel file:")
    for i, sheet_name in enumerate(sheet_names):
        print(f"  {i+1}. {sheet_name}")
    
    # Read each sheet and display basic information
    for sheet_name in sheet_names:
        print(f"\n--- Sheet: {sheet_name} ---")
        df = xl.parse(sheet_name)
        print(f"Shape: {df.shape}")
        print("Columns:", list(df.columns))
        print("\nFirst 5 rows:")
        print(df.head())
        print("\nData types:")
        print(df.dtypes)
        
except Exception as e:
    print(f"Error reading Excel file: {e}")
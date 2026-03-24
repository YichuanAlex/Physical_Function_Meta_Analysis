import pandas as pd
import numpy as np
import os

# Function to extract sub-tables from the main Excel file with correct boundaries
def extract_subtables():
    excel_path = '/Users/jiangzixi/Downloads/出图/CMA- analysis.xlsx'
    xl = pd.ExcelFile(excel_path)
    df = xl.parse('Sheet1')
    
    # Define the sub-tables with correct row ranges based on user's structure
    subtables = {
        'grip_strength': df.iloc[0:10, :9],  # Includes header and 9 data rows
        '30CST': df.iloc[12:17, :9],         # Includes header and 4 data rows
        'FTSST': df.iloc[19:23, :9],         # Includes header and 2 data rows
        'muscle_mass': df.iloc[24:32, :9],    # Includes header and 6 data rows (added Zhang 2025)
        'MFES': df.iloc[34:37, :9],          # Includes header and 2 data rows
        'gait_speed': df.iloc[39:42, :9],     # Includes header and 2 data rows
        'TUG': df.iloc[44:49, :9]            # Includes header and 4 data rows
    }
    
    # Create directory for sub-tables
    subtables_dir = '/Users/jiangzixi/Downloads/出图/subtables_correct'
    os.makedirs(subtables_dir, exist_ok=True)
    
    # Clean and save each sub-table
    for name, table in subtables.items():
        print(f"\nProcessing {name}:")
        print("Original table:")
        print(table)
        
        # Handle special case for gait_speed table
        if name == 'gait_speed':
            # The header is split between rows 39 and 40
            # Use row 39 for the first column name
            table_clean = table[1:].copy()
            # Combine the column names from rows 39 and 40
            cols = ['Gait speed'] + list(table.iloc[1, 1:9])
            table_clean.columns = cols
        else:
            # Normal handling
            header = table.iloc[0]
            table_clean = table[1:].copy()
            table_clean.columns = header
        
        # Reset index
        table_clean.reset_index(drop=True, inplace=True)
        
        # Save to Excel
        output_path = os.path.join(subtables_dir, f'{name}.xlsx')
        table_clean.to_excel(output_path, index=False)
        print(f'\nCleaned table:')
        print(table_clean)
        print(f'Saved {name} to {output_path}')
    
    return subtables_dir

# Main function
if __name__ == '__main__':
    extract_subtables()
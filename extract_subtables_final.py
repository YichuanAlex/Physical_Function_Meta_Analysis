import pandas as pd
import numpy as np
import os

# Function to extract sub-tables from the main Excel file with correct header handling
def extract_subtables():
    excel_path = '/Users/jiangzixi/Downloads/出图/CMA- analysis.xlsx'
    xl = pd.ExcelFile(excel_path)
    df = xl.parse('Sheet1')
    
    # Define table boundaries based on user's structure
    table_boundaries = {
        'grip_strength': {'start': 0, 'end': 10},
        '30CST': {'start': 12, 'end': 17},
        'FTSST': {'start': 19, 'end': 23},
        'muscle_mass': {'start': 24, 'end': 32},
        'MFES': {'start': 34, 'end': 37},
        'gait_speed': {'start': 39, 'end': 42},
        'TUG': {'start': 44, 'end': 49}
    }
    
    # Create directory for sub-tables
    subtables_dir = '/Users/jiangzixi/Downloads/出图/subtables_correct'
    os.makedirs(subtables_dir, exist_ok=True)
    
    # Clean and save each sub-table
    for name, bounds in table_boundaries.items():
        print(f"\nProcessing {name}:")
        
        # Extract the specific rows for this table
        table = df.iloc[bounds['start']:bounds['end'], :9].copy()
        
        # Handle each table type specifically
        if name == 'gait_speed':
            # Special case: first row has numbers 1-6, second row has actual header
            # First row (index 39) has columns: 6, study, Mean, SD, n, Mean, SD, n, sub
            # Second row (index 40) has the actual header
            table_clean = table.copy()
            
            # Set column names
            column_names = ['index', 'study', 'exp_mean', 'exp_sd', 'exp_n', 
                           'ctrl_mean', 'ctrl_sd', 'ctrl_n', 'sub']
            table_clean.columns = column_names
            
            # Remove the first row (index 39) which contains numbers 1-6
            table_clean = table_clean.iloc[1:].copy()
            
            # Add the outcome measure name as a new column
            table_clean['outcome'] = 'Gait speed'
            
        else:
            # Normal case: first row has the outcome measure, second row has header
            table_clean = table.copy()
            
            # Extract outcome measure from first row
            outcome = table_clean.iloc[0, 0]
            
            # Extract header from second row
            header_row = table_clean.iloc[0]
            
            # Set column names with proper names
            if header_row.iloc[0] == outcome:
                # First column has outcome, then study, then experimental, then control
                column_names = ['outcome', 'study', 'exp_mean', 'exp_sd', 'exp_n', 
                               'ctrl_mean', 'ctrl_sd', 'ctrl_n', 'sub']
            else:
                # First column might have numbers or other identifiers
                column_names = ['index', 'study', 'exp_mean', 'exp_sd', 'exp_n', 
                               'ctrl_mean', 'ctrl_sd', 'ctrl_n', 'sub']
                
            table_clean.columns = column_names
            
            # Remove the header row
            table_clean = table_clean.iloc[1:].copy()
            
            # Set outcome column if it exists
            if 'outcome' in table_clean.columns and pd.isna(table_clean['outcome']).all():
                table_clean['outcome'] = outcome
        
        # Drop any completely empty rows
        table_clean = table_clean.dropna(how='all').reset_index(drop=True)
        
        # Clean up numeric columns
        numeric_columns = ['exp_mean', 'exp_sd', 'exp_n', 'ctrl_mean', 'ctrl_sd', 'ctrl_n']
        for col in numeric_columns:
            if col in table_clean.columns:
                try:
                    table_clean[col] = pd.to_numeric(table_clean[col])
                except ValueError:
                    # If conversion fails, keep as is
                    pass
        
        print(f'\nCleaned table:')
        print(table_clean)
        print(f'Table shape: {table_clean.shape}')
        
        # Save to Excel
        output_path = os.path.join(subtables_dir, f'{name}.xlsx')
        table_clean.to_excel(output_path, index=False)
        print(f'Saved {name} to {output_path}')
    
    return subtables_dir

# Main function
if __name__ == '__main__':
    extract_subtables()
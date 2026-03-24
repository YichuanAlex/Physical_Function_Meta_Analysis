import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from rpy2.robjects.packages import importr
import rpy2.robjects as robjects
import metap
import warnings
warnings.filterwarnings('ignore')

# Import R packages
metafor = importr('metafor')
graphics = importr('graphics')

# Set R options
robjects.r('options(warn = -1)')

# Set plot style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('colorblind')

# Function to extract sub-tables from the main Excel file
def extract_subtables():
    excel_path = '/Users/jiangzixi/Downloads/出图/CMA- analysis.xlsx'
    xl = pd.ExcelFile(excel_path)
    df = xl.parse('Sheet1')
    
    # Define the sub-tables based on the analysis
    subtables = {
        'grip_strength': df.iloc[0:10, :9],
        '30CST': df.iloc[12:17, :8],
        'FTSST': df.iloc[19:23, :8],
        'muscle_mass': df.iloc[24:31, :8],
        'MFES': df.iloc[34:37, :8],
        'gait_speed': df.iloc[40:42, :9],
        'TUG': df.iloc[44:49, :8]
    }
    
    # Create directory for sub-tables
    subtables_dir = '/Users/jiangzixi/Downloads/出图/subtables'
    os.makedirs(subtables_dir, exist_ok=True)
    
    # Clean and save each sub-table
    for name, table in subtables.items():
        # Set proper column names
        header = table.iloc[0]
        table_clean = table[1:].copy()
        table_clean.columns = header
        
        # Reset index
        table_clean.reset_index(drop=True, inplace=True)
        
        # Save to Excel
        output_path = os.path.join(subtables_dir, f'{name}.xlsx')
        table_clean.to_excel(output_path, index=False)
        print(f'Saved {name} to {output_path}')
    
    return subtables_dir

# Function to load a sub-table and prepare it for meta-analysis
def load_table(table_path):
    df = pd.read_excel(table_path)
    
    # Print dataframe info for debugging
    print(f"\nTable info for {table_path}:")
    print(df.columns.tolist())
    print(df.head())
    
    # Extract study names
    studies = df['study'].tolist()
    
    # Handle different column name patterns
    if 'Mean.1' in df.columns and 'SD.1' in df.columns and 'n.1' in df.columns:
        # Experimental group
        exp_mean = df['Mean'].astype(float)
        exp_sd = df['SD'].astype(float)
        exp_n = df['n'].astype(int)
        
        # Control group
        ctrl_mean = df['Mean.1'].astype(float)
        ctrl_sd = df['SD.1'].astype(float)
        ctrl_n = df['n.1'].astype(int)
    elif 'Mean' in df.columns and 'SD' in df.columns and 'n' in df.columns:
        # For tables where control group columns might be named differently
        exp_mean = df['Mean'].astype(float)
        exp_sd = df['SD'].astype(float)
        exp_n = df['n'].astype(int)
        
        # In some tables, control columns might have different names
        ctrl_mean = df['Mean'].astype(float)  # Default, will be overridden if possible
        ctrl_sd = df['SD'].astype(float)      # Default, will be overridden if possible
        ctrl_n = df['n'].astype(int)          # Default, will be overridden if possible
        
        # Look for alternative control column names
        for col in df.columns:
            if 'Mean' in col and col != 'Mean':
                ctrl_mean = df[col].astype(float)
            if 'SD' in col and col != 'SD':
                ctrl_sd = df[col].astype(float)
            if 'n' in col and col != 'n':
                ctrl_n = df[col].astype(int)
    else:
        raise ValueError(f"Could not identify proper columns in {table_path}")
    
    # Calculate standardized mean difference (SMD) and its variance
    smd, var = calculate_smd(exp_mean, exp_sd, exp_n, ctrl_mean, ctrl_sd, ctrl_n)
    
    return smd, var, studies

# Function to calculate SMD and variance
def calculate_smd(exp_mean, exp_sd, exp_n, ctrl_mean, ctrl_sd, ctrl_n):
    # Calculate pooled standard deviation
    pooled_sd = np.sqrt(
        ((exp_n - 1) * exp_sd**2 + (ctrl_n - 1) * ctrl_sd**2) / 
        (exp_n + ctrl_n - 2)
    )
    
    # Calculate SMD (Hedges' g)
    smd = (exp_mean - ctrl_mean) / pooled_sd
    
    # Calculate variance of SMD
    var = (1/exp_n + 1/ctrl_n) + (smd**2) / (2 * (exp_n + ctrl_n))
    
    return smd, var

# Function to create forest plot
def create_forest_plot(smd, var, studies, output_path):
    # Convert Python data to R objects
    r_smd = robjects.FloatVector(smd)
    r_var = robjects.FloatVector(var)
    r_studies = robjects.StrVector(studies)
    r_output_path = robjects.StrVector([output_path])
    
    # Run R code for forest plot
    robjects.r('''
    create_forest <- function(smd, var, studies, output_path) {
        # Fit random-effects model
        res <- rma(yi=smd, vi=var, method='DL')
        
        # Create forest plot
        png(output_path, width=1000, height=600, res=300)
        forest(res, slab=studies, xlab='Standardized Mean Difference', 
               mlab='Summary Effect', alim=c(-2, 2))
        dev.off()
        
        # Return results
        return(list(ci_lb=res$ci.lb, ci_ub=res$ci.ub, pval=res$pval))
    }
    ''')
    
    # Call the R function
    r_function = robjects.globalenv['create_forest']
    result = r_function(r_smd, r_var, r_studies, r_output_path[0])
    
    # Create a simple result object with the information needed
    class Result:
        def __init__(self, ci_lb, ci_ub, pval):
            self.ci = type('obj', (object,), {'lb': ci_lb, 'ub': ci_ub})
            self.pval = pval
    
    return Result(result[0][0], result[1][0], result[2][0])

# Function to create funnel plot
def create_funnel_plot(smd, var, output_path):
    # Convert Python data to R objects
    r_smd = robjects.FloatVector(smd)
    r_var = robjects.FloatVector(var)
    r_output_path = robjects.StrVector([output_path])
    
    # Run R code for funnel plot
    robjects.r('''
    create_funnel <- function(smd, var, output_path) {
        # Fit random-effects model
        res <- rma(yi=smd, vi=var, method='DL')
        
        # Create funnel plot
        png(output_path, width=800, height=600, res=300)
        funnel(res, xlab='Standardized Mean Difference', ylab='Standard Error')
        dev.off()
    }
    ''')
    
    # Call the R function
    r_function = robjects.globalenv['create_funnel']
    r_function(r_smd, r_var, r_output_path[0])

# Function to perform Fail-Safe N analysis
def perform_fail_safe_n(smd, var, studies):
    # Use metap package for fail-safe N
    res = metap.smd(smd, np.sqrt(var), studies)
    fail_safe_n = metap.failsafe(res)
    
    return fail_safe_n

# Function to perform trim-and-fill analysis
def perform_trimfill(smd, var, studies, output_path):
    # Convert Python data to R objects
    r_smd = robjects.FloatVector(smd)
    r_var = robjects.FloatVector(var)
    r_output_path = robjects.StrVector([output_path])
    
    # Run R code for trim-and-fill analysis
    robjects.r('''
    perform_trimfill <- function(smd, var, output_path) {
        # Fit random-effects model
        res <- rma(yi=smd, vi=var, method='DL')
        
        # Perform trim-and-fill
        tf <- trimfill(res)
        
        # Create funnel plot with trim-and-fill
        png(output_path, width=800, height=600, res=300)
        funnel(tf, xlab='Standardized Mean Difference', ylab='Standard Error')
        dev.off()
        
        # Return results
        return(list(ks=tf$ks, b=tf$b, se=tf$se, ci_lb=tf$ci.lb, ci_ub=tf$ci.ub))
    }
    ''')
    
    # Call the R function
    r_function = robjects.globalenv['perform_trimfill']
    result = r_function(r_smd, r_var, r_output_path[0])
    
    # Create a simple result object with the information needed
    class TrimFillResult:
        def __init__(self, ks, b, se, ci_lb, ci_ub):
            self.ks = ks
            self.b = b
            self.se = se
            self.ci = type('obj', (object,), {'lb': ci_lb, 'ub': ci_ub})
    
    return TrimFillResult(result[0][0], result[1][0], result[2][0], result[3][0], result[4][0])

# Function to generate caption.md file
def generate_caption(caption_path, analysis_type, table_name, results):
    with open(caption_path, 'w') as f:
        f.write(f'# {analysis_type} Analysis for {table_name}\n\n')
        f.write('## Analysis Results\n\n')
        
        if analysis_type == 'Forest Plot':
            f.write('### Random-Effects Model Results\n\n')
            f.write(f'Summary Effect (SMD): {results.ci.lb:.3f} to {results.ci.ub:.3f}, p = {results.pval:.3f}\n\n')
            f.write('### Plot Description\n\n')
            f.write('The forest plot displays the standardized mean difference (SMD) for each study ') 
            f.write('along with its 95% confidence interval. The diamond at the bottom represents ') 
            f.write('the summary effect from the random-effects model.\n\n')
            
        elif analysis_type == 'Funnel Plot':
            f.write('### Publication Bias Assessment\n\n')
            f.write('The funnel plot assesses publication bias by plotting study effect sizes against their standard errors. ') 
            f.write('A symmetric funnel shape suggests minimal publication bias.\n\n')
            
        elif analysis_type == 'Fail-Safe N':
            f.write('### Fail-Safe N Results\n\n')
            f.write(f'Fail-Safe N (Rosenthal): {results}\n\n')
            f.write('The Fail-Safe N indicates the number of unpublished studies with null results ') 
            f.write('that would be needed to make the combined effect statistically non-significant.\n\n')
            
        elif analysis_type == 'Trim-and-Fill':
            f.write('### Trim-and-Fill Results\n\n')
            f.write(f'Number of studies trimmed: {tf.ks}\n')
            f.write(f'Adjusted summary effect: {tf.ci.lb:.3f} to {tf.ci.ub:.3f}\n\n')
            f.write('The trim-and-fill method adjusts for publication bias by trimming asymmetrically ') 
            f.write('distributed studies and imputing their symmetric counterparts.\n\n')
            
        f.write('## Methods\n\n')
        f.write('All analyses were performed using the metafor package in R and metap package in Python. ') 
        f.write('Random-effects models were used with the DerSimonian-Laird estimator.\n\n')
        
        f.write('## Data Sources\n\n')
        f.write('Data extracted from the original Excel file: CMA- analysis.xlsx\n')

# Main function to perform all analyses
def main():
    # Step 1: Extract sub-tables
    subtables_dir = extract_subtables()
    
    # Step 2: Create directories for each analysis method
    methods = ['forest_plot', 'funnel_plot', 'fail_safe_n', 'trim_fill']
    for method in methods:
        method_dir = os.path.join('/Users/jiangzixi/Downloads/出图', method)
        os.makedirs(method_dir, exist_ok=True)
    
    # Step 3: Process each sub-table
    for table_file in os.listdir(subtables_dir):
        if table_file.endswith('.xlsx'):
            table_path = os.path.join(subtables_dir, table_file)
            table_name = os.path.splitext(table_file)[0]
            
            print(f'\nProcessing {table_name}...')
            
            try:
                # Load and prepare data
                smd, var, studies = load_table(table_path)
                
                # 1. Forest Plot Analysis
                forest_dir = os.path.join('/Users/jiangzixi/Downloads/出图', 'forest_plot')
                forest_output = os.path.join(forest_dir, f'{table_name}_forest.png')
                res = create_forest_plot(smd, var, studies, forest_output)
                
                # Generate caption
                forest_caption = os.path.join(forest_dir, f'{table_name}_caption.md')
                generate_caption(forest_caption, 'Forest Plot', table_name, res)
                
                # 2. Funnel Plot Analysis
                funnel_dir = os.path.join('/Users/jiangzixi/Downloads/出图', 'funnel_plot')
                funnel_output = os.path.join(funnel_dir, f'{table_name}_funnel.png')
                create_funnel_plot(smd, var, funnel_output)
                
                # Generate caption
                funnel_caption = os.path.join(funnel_dir, f'{table_name}_caption.md')
                generate_caption(funnel_caption, 'Funnel Plot', table_name, None)
                
                # 3. Fail-Safe N Analysis
                fail_safe_dir = os.path.join('/Users/jiangzixi/Downloads/出图', 'fail_safe_n')
                fail_safe_n = perform_fail_safe_n(smd, var, studies)
                
                # Save results to Excel
                fail_safe_df = pd.DataFrame({'Fail-Safe N': [fail_safe_n]})
                fail_safe_df.to_excel(os.path.join(fail_safe_dir, f'{table_name}_failsafe.xlsx'), index=False)
                
                # Generate caption
                fail_safe_caption = os.path.join(fail_safe_dir, f'{table_name}_caption.md')
                generate_caption(fail_safe_caption, 'Fail-Safe N', table_name, fail_safe_n)
                
                # 4. Trim-and-Fill Analysis
                trim_fill_dir = os.path.join('/Users/jiangzixi/Downloads/出图', 'trim_fill')
                trim_fill_output = os.path.join(trim_fill_dir, f'{table_name}_trimfill.png')
                tf = perform_trimfill(smd, var, studies, trim_fill_output)
                
                # Save results to Excel
                trim_fill_results = {
                    'Studies Trimmed': [tf.ks],
                    'Adjusted SMD': [tf.b],
                    'Adjusted SE': [tf.se]
                }
                trim_fill_df = pd.DataFrame(trim_fill_results)
                trim_fill_df.to_excel(os.path.join(trim_fill_dir, f'{table_name}_trimfill.xlsx'), index=False)
                
                # Generate caption
                trim_fill_caption = os.path.join(trim_fill_dir, f'{table_name}_caption.md')
                generate_caption(trim_fill_caption, 'Trim-and-Fill', table_name, tf)
                
                print(f'Successfully analyzed {table_name}')
                
            except Exception as e:
                print(f'Error processing {table_name}: {e}')

if __name__ == '__main__':
    main()
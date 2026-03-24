import pandas as pd
import numpy as np
import os

# Function to calculate mean difference (MD) and its variance
def calculate_md(exp_mean, exp_sd, exp_n, ctrl_mean, ctrl_sd, ctrl_n, outcome=None):
    # For FTSST and TUG, lower values are better, so invert the difference
    if outcome in ['FTSST', 'TUG']:
        md = (ctrl_mean - exp_mean)  # Invert for better interpretation
    else:
        md = (exp_mean - ctrl_mean)  # Standard calculation
    
    # Calculate variance of MD
    var = (exp_sd**2 / exp_n) + (ctrl_sd**2 / ctrl_n)
    
    return md, var

# Function to calculate random effects summary for a subgroup
def calculate_subgroup_summary(md, var):
    k = len(md)
    if k == 0:
        return None, None, None, None
    
    # Fixed effects weights
    fe_weights = 1 / var
    
    # Calculate Q statistic
    fe_summary = np.sum(fe_weights * md) / np.sum(fe_weights)
    Q = np.sum(fe_weights * (md - fe_summary)**2)
    
    # Calculate I²
    df = k - 1
    if Q > df:
        I_squared = (Q - df) / Q * 100
    else:
        I_squared = 0
    
    # Calculate tau-squared
    if Q > df:
        tau_squared = (Q - df) / (np.sum(fe_weights) - np.sum(fe_weights**2) / np.sum(fe_weights))
    else:
        tau_squared = 0
    
    # Random effects weights and summary
    re_weights = 1 / (var + tau_squared)
    summary_md = np.sum(re_weights * md) / np.sum(re_weights)
    summary_var = 1 / np.sum(re_weights)
    summary_ci_lower = summary_md - 1.96 * np.sqrt(summary_var)
    summary_ci_upper = summary_md + 1.96 * np.sqrt(summary_var)
    
    return {
        'subgroup_size': k,
        'md': summary_md,
        'ci_lower': summary_ci_lower,
        'ci_upper': summary_ci_upper,
        'i_squared': I_squared
    }

# Main subgroup analysis function
def perform_subgroup_analysis():
    subtables_dir = '/Users/jiangzixi/Downloads/出图/subtables_academic'
    
    # Define outcome measures and intervention types
    interventions = ['Baduanjin', 'Tai-chi', 'Yijinjing']
    
    # Store results
    subgroup_results = []
    
    # Process each sub-table
    for table_file in os.listdir(subtables_dir):
        if table_file.endswith('.xlsx'):
            table_path = os.path.join(subtables_dir, table_file)
            outcome_name = os.path.splitext(table_file)[0].replace('_', ' ')
            
            print(f'\n=== Analyzing {outcome_name} ===')
            
            try:
                # Load data
                df = pd.read_excel(table_path)
                
                # Get all unique interventions in this outcome
                available_interventions = df['sub'].unique()
                
                for intervention in interventions:
                    if intervention in available_interventions:
                        # Filter data for this intervention
                        subgroup_data = df[df['sub'] == intervention]
                        
                        if len(subgroup_data) > 0:
                            # Calculate MD and variance for this subgroup
                            exp_mean = subgroup_data['exp_mean'].astype(float)
                            exp_sd = subgroup_data['exp_sd'].astype(float)
                            exp_n = subgroup_data['exp_n'].astype(int)
                            ctrl_mean = subgroup_data['ctrl_mean'].astype(float)
                            ctrl_sd = subgroup_data['ctrl_sd'].astype(float)
                            ctrl_n = subgroup_data['ctrl_n'].astype(int)
                            
                            md, var = calculate_md(exp_mean, exp_sd, exp_n, ctrl_mean, ctrl_sd, ctrl_n, outcome_name)
                            
                            # Calculate summary statistics
                            result = calculate_subgroup_summary(md, var)
                            
                            if result is not None:
                                subgroup_results.append({
                                    'outcome': outcome_name,
                                    'intervention': intervention,
                                    'subgroup_size': result['subgroup_size'],
                                    'md': result['md'],
                                    'ci_lower': result['ci_lower'],
                                    'ci_upper': result['ci_upper'],
                                    'i_squared': result['i_squared'],
                                    'significant': result['ci_lower'] > 0 or result['ci_upper'] < 0
                                })
                                
                                # Print results
                                print(f'{intervention}:')
                                print(f'  Studies: {result["subgroup_size"]}')
                                print(f'  MD = {result["md"]:.3f} (95% CI: {result["ci_lower"]:.3f} to {result["ci_upper"]:.3f})')
                                print(f'  I² = {result["i_squared"]:.1f}%')
                                print(f'  Statistically significant: {result["ci_lower"] > 0}')
                    else:
                        print(f'{intervention}: No data available')
                        
            except Exception as e:
                print(f'Error analyzing {outcome_name}: {e}')
    
    # Create summary dataframe
    results_df = pd.DataFrame(subgroup_results)
    
    # Save results to Excel
    results_df.to_excel('/Users/jiangzixi/Downloads/出图/subgroup_analysis_results.xlsx', index=False)
    
    return results_df

# Run the analysis if this script is executed directly
if __name__ == '__main__':
    results = perform_subgroup_analysis()
    print('\n=== Subgroup Analysis Complete ===')
    print(f'Results saved to subgroup_analysis_results.xlsx')

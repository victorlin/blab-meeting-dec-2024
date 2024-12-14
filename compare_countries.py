import csv
import pandas as pd

def calculate_percent_change(old_file, new_file):
    # Read CSV files
    old_df = pd.read_csv(old_file)
    new_df = pd.read_csv(new_file)
    
    # Merge dataframes on country name
    merged_df = pd.merge(old_df, new_df, on='name', suffixes=('_nextstrain', '_nextclade'))
    
    # Calculate percent change
    merged_df['percent_change'] = ((merged_df['visitors_nextclade'] - merged_df['visitors_nextstrain']) / merged_df['visitors_nextstrain']) * 100
    
    # Sort by visitors_nextclade in descending order
    result_df = merged_df[['name', 'visitors_nextstrain', 'visitors_nextclade', 'percent_change']]
    result_df = result_df.sort_values(by='visitors_nextclade', ascending=False)
    
    # Print results
    print("Country Visitor Percent Changes:")
    print(result_df.to_string(index=False))
    
    # Optional: Save results to CSV
    result_df.to_csv('visitor_percent_changes.csv', index=False)

# Specify file paths
old_file = '/Users/victor/Downloads/lab-meeting/nextstrain-2024/countries.csv'
new_file = '/Users/victor/Downloads/lab-meeting/nextclade-2024/countries.csv'

# Run the comparison
calculate_percent_change(old_file, new_file)

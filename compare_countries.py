import pandas as pd
import plotly.express as px
import pycountry

def get_country_code(country_name):
    """Convert country name to ISO alpha-3 code"""
    try:
        # Special cases for some countries
        country_mapping = {
            'United States': 'USA',
            'United Kingdom': 'GBR',
            'China': 'CHN',
            'Japan': 'JPN',
            'Brazil': 'BRA',
            'France': 'FRA',
            'Spain': 'ESP',
            'Italy': 'ITA',
            'Australia': 'AUS',
            'India': 'IND',
            'Canada': 'CAN',
            'Germany': 'DEU'
        }
        
        if country_name in country_mapping:
            return country_mapping[country_name]
        
        return pycountry.countries.search_fuzzy(country_name)[0].alpha_3
    except Exception:
        return None

def calculate_percent_change(old_file, new_file):
    # Read CSV files
    old_df = pd.read_csv(old_file)
    new_df = pd.read_csv(new_file)
    
    # Merge dataframes on country name
    merged_df = pd.merge(old_df, new_df, on='name', suffixes=('_old', '_new'))
    
    # Calculate percent change
    merged_df['percent_change'] = ((merged_df['visitors_new'] - merged_df['visitors_old']) / merged_df['visitors_old']) * 100
    
    # Add country codes
    merged_df['country_code'] = merged_df['name'].apply(get_country_code)
    
    # Sort by visitors_new in descending order
    result_df = merged_df[['name', 'country_code', 'visitors_old', 'visitors_new', 'percent_change']]
    result_df = result_df.sort_values(by='visitors_new', ascending=False)
    
    # Print results
    print("Country Visitor Percent Changes:")
    print(result_df.to_string(index=False))
    
    # Create interactive map
    fig = px.choropleth(
        result_df, 
        locations='country_code', 
        color='percent_change',
        hover_name='name',
        color_continuous_scale='RdYlGn',
        title='Visitor Percent Change by Country',
        hover_data={
            'name': True, 
            'visitors_old': ':.0f', 
            'visitors_new': ':.0f', 
            'percent_change': ':.2f%',
            'country_code': False
        }
    )
    
    # Customize layout
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        )
    )
    
    # Save the plot
    fig.write_html('visitor_changes_map.html')
    
    # Save results to CSV
    result_df.to_csv('visitor_percent_changes.csv', index=False)
    
    return result_df, fig

# Specify file paths
old_file = '/Users/victor/Downloads/lab-meeting/nextstrain-2024/countries.csv'
new_file = '/Users/victor/Downloads/lab-meeting/nextclade-2024/countries.csv'

# Run the comparison and generate map
df, fig = calculate_percent_change(old_file, new_file)

# Save the plot to file
fig.write_image('visitor_changes_map.png', scale=2)

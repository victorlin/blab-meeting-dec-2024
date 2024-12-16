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

def calculate_percent_change(nextstrain_file, nextclade_file):
    # Read CSV files
    nextstrain_df = pd.read_csv(nextstrain_file)
    nextclade_df = pd.read_csv(nextclade_file)
    
    # Merge dataframes on country name
    merged_df = pd.merge(nextstrain_df, nextclade_df, on='name', suffixes=('_nextstrain', '_nextclade'))
    
    # Calculate percent change
    merged_df['percent_change'] = ((merged_df['visitors_nextclade'] - merged_df['visitors_nextstrain']) / merged_df['visitors_nextstrain']) * 100
    
    # Add country codes
    merged_df['country_code'] = merged_df['name'].apply(get_country_code)
    
    # Sort by visitors_nextclade in descending order
    result_df = merged_df[['name', 'country_code', 'visitors_nextstrain', 'visitors_nextclade', 'percent_change']]
    result_df = result_df.sort_values(by='visitors_nextclade', ascending=False)
    
    # Print results
    print("Country Visitor Percent Changes:")
    print(result_df.to_string(index=False))
    
    # Create interactive map
    fig = px.choropleth(
        result_df, 
        locations='country_code', 
        color='percent_change',
        hover_name='name',
        color_continuous_scale=[
            [0.0, 'yellow'],
            [0.5, 'white'],
            [1.0, 'blue']
        ],
        title='Ratio of website visitors Nextclade : Nextstrain',
        color_continuous_midpoint=0,
        range_color=[-100, 100],
        hover_data={
            'name': True, 
            'visitors_nextstrain': ':.0f', 
            'visitors_nextclade': ':.0f', 
            'percent_change': ':.2f%',
            'country_code': False
        }
    )
    
    # Customize layout
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        coloraxis_colorbar=dict(
            title='',
            tickvals=[-100, 0, 100],
            ticktext=['≤1:2', '1:1', '≥2:1']
        )
    )
    
    # Save the plot
    fig.write_html('index.html')
    
    return result_df, fig

# Specify file paths
nextstrain_file = 'nextstrain-2024/countries.csv'
nextclade_file = 'nextclade-2024/countries.csv'

# Run the comparison and generate map
df, fig = calculate_percent_change(nextstrain_file, nextclade_file)

# Save the plot to file
fig.write_image('visitor_changes_map.png', scale=2)

import pandas as pd
import json
import os
import plotly.express as px

def phmap(df):
    # df is now passed in; remove the CSV read
    # — Load GeoJSON —
    current_directory = os.getcwd()
    json_file = os.path.join(current_directory, 'ph.json')
    with open(json_file) as f:
        ph_geojson = json.load(f)

    # — Calculate total enrollees per region —
    enrollment_columns = [c for c in df.columns if ('Male' in c or 'Female' in c) and c != 'BEIS School ID']
    region_enrollment = df.groupby('Region')[enrollment_columns].sum().sum(axis=1).reset_index()
    region_enrollment.columns = ['Region', 'Total_Enrollees']

    # — Map region names to geojson ids —
      # Map region names from CSV to GeoJSON
    region_mapping = {
        'Region I': 'Ilocos',
        'Region II': 'Cagayan Valley',
        'Region III': 'Central Luzon',
        'Region IV-A': 'Calabarzon',
        'MIMAROPA': 'Mimaropa',
        'Region V': 'Bicol',
        'Region VI': 'Western Visayas',
        'Region VII': 'Central Visayas',
        'Region VIII': 'Eastern Visayas',
        'Region IX': 'Zamboanga Peninsula',
        'Region X': 'Northern Mindanao',
        'Region XI': 'Davao',
        'Region XII': 'Soccsksargen',
        'NCR': 'National Capital Region',
        'CAR': 'Cordillera Administrative Region',
        'BARMM': 'Autonomous Region in Muslim Mindanao',
        'CARAGA': 'Caraga'
    }

    region_enrollment['id'] = region_enrollment['Region'].map(region_mapping)

    # — Build the choropleth —
    fig = px.choropleth_mapbox(
        region_enrollment,
        geojson=ph_geojson,
        locations='id',
        color='Total_Enrollees',
        featureidkey='properties.name',
        center={'lat': 12.8797, 'lon': 121.7740},
        mapbox_style='carto-positron',
        zoom=5,
        color_continuous_scale=[
            [0.0, '#0174DF'],
            [0.33, '#0154A2'],
            [0.66, '#DE082C'],
            [1.0, '#F2EC1A']
        ],
        labels={'Total_Enrollees': 'Total Enrollees'},
        hover_data={'Region': True, 'Total_Enrollees': True}
    )
    fig.update_traces(hovertemplate="<b>%{location}</b><br>Total Enrollees: %{z}<extra></extra>")
    fig.update_layout(height=800, margin={'r':0,'t':0,'l':0,'b':0})

    return fig


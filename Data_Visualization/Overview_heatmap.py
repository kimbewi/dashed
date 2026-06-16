import pandas as pd
import numpy as np
from dash import dcc
import plotly.graph_objects as go

def get_region_heatmap_figure(df, selected_level='All'):
    if df is None or df.empty:
        df = pd.read_csv("CSV Files/CLEANED_SY2023_Enrollment.csv")

    # Define combined levels
    combined_levels = {
        'Kindergarten': ['K Male', 'K Female'],
        'ELEM': [
            'G1 Male', 'G1 Female', 'G2 Male', 'G2 Female', 'G3 Male', 'G3 Female',
            'G4 Male', 'G4 Female', 'G5 Male', 'G5 Female', 'G6 Male', 'G6 Female',
            'Elem NG Male', 'Elem NG Female'
        ],
        'JHS': [
            'G7 Male', 'G7 Female', 'G8 Male', 'G8 Female', 'G9 Male', 'G9 Female',
            'G10 Male', 'G10 Female', 'JHS NG Male', 'JHS NG Female'
        ],
        'SHS': [
            'G11 ACAD ABM Male', 'G11 ACAD ABM Female', 'G11 ACAD HUMSS Male', 'G11 ACAD HUMSS Female',
            'G11 ACAD STEM Male', 'G11 ACAD STEM Female', 'G11 ACAD GAS Male', 'G11 ACAD GAS Female',
            'G11 ACAD PBM Male', 'G11 ACAD PBM Female', 'G11 TVL Male', 'G11 TVL Female',
            'G11 SPORTS Male', 'G11 SPORTS Female', 'G11 ARTS Male', 'G11 ARTS Female',
            'G12 ACAD ABM Male', 'G12 ACAD ABM Female', 'G12 ACAD HUMSS Male', 'G12 ACAD HUMSS Female',
            'G12 ACAD STEM Male', 'G12 ACAD STEM Female', 'G12 ACAD GAS Male', 'G12 ACAD GAS Female',
            'G12 ACAD PBM Male', 'G12 ACAD PBM Female', 'G12 TVL Male', 'G12 TVL Female',
            'G12 SPORTS Male', 'G12 SPORTS Female', 'G12 ARTS Male', 'G12 ARTS Female'
        ]
    }

    # Sum up enrollment data
    enrollment_columns = [col for cols in combined_levels.values() for col in cols]
    region_level_totals = df.groupby('Region').agg({col: 'sum' for col in enrollment_columns}).reset_index()

    region_heatmap_data = pd.DataFrame()
    region_heatmap_data['Region'] = region_level_totals['Region']

    for level, columns in combined_levels.items():
        region_heatmap_data[level] = region_level_totals[columns].sum(axis=1)

    # Added Total NG column
    ng_columns = ['Elem NG Male', 'Elem NG Female', 'JHS NG Male', 'JHS NG Female']
    region_heatmap_data['Total NG'] = region_level_totals[ng_columns].sum(axis=1)

    region_heatmap_data['Subtotal'] = region_heatmap_data[['Kindergarten', 'ELEM', 'JHS', 'SHS']].sum(axis=1) # Don't include Total NG in the subtotal

    # Add Grand Total row
    grand_totals = region_heatmap_data[['Kindergarten', 'ELEM', 'JHS', 'SHS', 'Total NG', 'Subtotal']].sum()
    grand_total_row = pd.DataFrame([['Grand Total'] + grand_totals.tolist()], columns=region_heatmap_data.columns)

    region_heatmap_data = pd.concat([region_heatmap_data, grand_total_row], ignore_index=True)
    region_heatmap_data = region_heatmap_data.iloc[::-1].reset_index(drop=True)

    # Select the data for display
    # April 25, 2025 changes: added total NG in display_data
    if selected_level == 'All':
        display_data = region_heatmap_data.set_index('Region').loc[:, ['Kindergarten', 'ELEM', 'JHS', 'SHS', 'Total NG', 'Subtotal']]
        x_axis = ['Kindergarten', 'ELEM', 'JHS', 'SHS', 'Total NG', 'Subtotal']
    else:
        display_data = region_heatmap_data.set_index('Region').loc[:, [selected_level]]
        x_axis = [selected_level]

    y_axis = display_data.index.tolist()
    z = display_data.values

    # Code for minimum/maximum coloring!!
    # To exclude Grand Total from the min/max logic
    filtered = display_data.drop(index='Grand Total', errors='ignore')
    # Determine min/max rows
    max_idx = filtered[selected_level].idxmax() if selected_level != 'All' else filtered['Subtotal'].idxmax()
    min_idx = filtered[selected_level].idxmin() if selected_level != 'All' else filtered['Subtotal'].idxmin()

    # Create mask for color mapping
    colors = np.full_like(z, fill_value=0, dtype=int)

    for i, region in enumerate(y_axis):
        for j, level in enumerate(x_axis):
            if region == max_idx:
                colors[i][j] = 1  # Max
            elif region == min_idx:
                colors[i][j] = -1  # Min
            elif region == 'Grand Total':
                colors[i][j] = 2  # Grand Total
    
    # Normalize to [0, 1] for Plotly
    value_map = {-1: 0.0, # Min
                 0: 0.33, # Normal
                 1: 0.66, # Max
                 2: 1.0} # Grand Total
    
    # Map colors to normalized values
    normalized_colors = np.vectorize(value_map.get)(colors)     

    # Custom colorscale
    custom_colorscale = [
        [0.0, '#DE082C'],  
        [0.33, '#F7FBFE'],  
        [0.66, '#F2EC1A'],  
        [1.0, '#084683']     
    ]

    # Use a blue colorscale (temporarily commented out)
    # custom_colorscale = 'Blues'

    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        showscale=False, # Hide color scale
        z=normalized_colors,
        x=x_axis,
        y=y_axis,
        text=z,
        texttemplate="%{text}",
        colorscale=custom_colorscale,
        colorbar=dict(title='Enrollment'),  # Shows color bar on the side
        xgap=1,  # Horizontal grid space
        ygap=1   # Vertical grid space
    ))

    fig.update_layout(
        title=f"Enrollment Heatmap by Region - {selected_level if selected_level != 'All' else 'All Levels'}",
        title_font=dict(
            family="Google Sans, sans-serif",
            size=24,
            color="#DE082C"
        ),
        xaxis=dict(title="Education Level", side="top"),
        yaxis_title="Region",
        plot_bgcolor='#C9E1E6',
        height=800,
        width=800,
        margin=dict(l=100, r=50, t=100, b=100),
        font=dict(size=10)
    )

    return fig
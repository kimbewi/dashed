import pandas as pd
import plotly.express as px


def gender_bar(df = None):
    # Load dataset
    if df is None:
            df = pd.read_csv("CSV Files/CLEANED_SY2023_Enrollment.csv")

    # Melt the DataFrame
    # This will convert the DataFrame from wide format to long format
    # Each row will represent a single enrollment count for a specific descriptor and region
    melted_df = df.melt(id_vars=["Region"], var_name="Descriptor", value_name="Enrollees")

    # Grade Level Dictionary
    combined_levels = {
        'K': ['K Male', 'K Female'],
        'ELEM': [
            'G1 Male', 'G1 Female', 'G2 Male', 'G2 Female',
            'G3 Male', 'G3 Female', 'G4 Male', 'G4 Female', 'G5 Male', 'G5 Female',
            'G6 Male', 'G6 Female', 'Elem NG Male', 'Elem NG Female'
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

    # Invert the combined_levels dict
    # This will create a mapping from descriptor to category
    descriptor_to_category = {
        descriptor: category
        for category, descriptors in combined_levels.items()
        for descriptor in descriptors
    }

    # Extract Gender
    melted_df['Gender'] = melted_df['Descriptor'].str.extract(r'(Male|Female)$')[0]

    # Map Category
    melted_df['Category'] = melted_df['Descriptor'].map(descriptor_to_category)

    # Clean data
    melted_df['Enrollees'] = pd.to_numeric(melted_df['Enrollees'], errors='coerce')
    melted_df.dropna(subset=['Category', 'Gender', 'Enrollees'], inplace=True)

    # Group data
    grouped = melted_df.groupby(['Category', 'Gender'], observed=False, as_index=False)['Enrollees'].sum()

    # Ensure correct category order
    category_order = ['K', 'ELEM', 'JHS', 'SHS']
    grouped['Category'] = pd.Categorical(grouped['Category'], categories=category_order, ordered=True)
    grouped = grouped.sort_values('Category')

    # Calculate percentage and label
    total_per_category = grouped.groupby('Category')['Enrollees'].transform('sum') # Total enrollees per category
    grouped['Percentage'] = (grouped['Enrollees'] / total_per_category) * 100 # Percentage of enrollees
    grouped['Label'] = grouped.apply( # Create label for each bar
        lambda row: f"{int(row['Enrollees']):,} ({row['Percentage']:.1f}%)", axis=1 # Format label
    )

        # Create stacked bar chart
    fig = px.bar(
        grouped, # Data for the bar chart
        x='Percentage', # X-axis: percentage of enrollees
        y='Category', # Y-axis: category (K, ELEM, JHS, SHS)
        color='Gender', # Color by command
        barmode='stack', # Stacked bar mode
        orientation='h', # Horizontal orientation
        text='Label', # Text on bars
        color_discrete_map={'Male': '#084683', 'Female': '#DE082C'}, # Color mapping
        title="Gender Distribution by Category (K, ELEM, JHS, SHS)" # Title of the chart
    )

    total_all = int(grouped['Enrollees'].sum()) # Total enrollees across all categories
    fig.update_layout(
       title={
            'text': f"Gender Distribution by Category (K, ELEM, JHS, SHS)<br><sub>Total Enrollees: {total_all:,}</sub>", # Title with total enrollees
            'x': 0.5 # Center the title
        },
        xaxis=dict( 
            title='Percentage', # X-axis title
             ticksuffix='%', # Suffix for ticks (can remove for cleanliness)
            range=[0, 100] # Range for X-axis
        ),
        yaxis_title='Category', # Y-axis title
        height=380, # Height of the chart
        legend_title='Gender', # Legend title
        margin=dict(l=20, r=20, t=60, b=0) # Margin settings
    )
    fig.update_traces(textposition='inside', insidetextanchor='middle') # Position labels inside bars

    return fig


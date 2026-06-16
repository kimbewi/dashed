import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict
import csv

# Load the dataset
file_path = "CSV Files/CLEANED_SY2023_Enrollment.csv"
df = pd.read_csv(file_path)

# Columns with enrollment data
enrollment_columns = [
    'K Male', 'K Female', 'G1 Male', 'G1 Female', 'G2 Male', 'G2 Female',
    'G3 Male', 'G3 Female', 'G4 Male', 'G4 Female', 'G5 Male', 'G5 Female',
    'G6 Male', 'G6 Female', 'Elem NG Male', 'Elem NG Female', 'G7 Male', 'G7 Female',
    'G8 Male', 'G8 Female', 'G9 Male', 'G9 Female', 'G10 Male', 'G10 Female',
    'JHS NG Male', 'JHS NG Female', 'G11 ACAD ABM Male', 'G11 ACAD ABM Female',
    'G11 ACAD HUMSS Male', 'G11 ACAD HUMSS Female', 'G11 ACAD STEM Male', 'G11 ACAD STEM Female',
    'G11 ACAD GAS Male', 'G11 ACAD GAS Female', 'G11 ACAD PBM Male', 'G11 ACAD PBM Female',
    'G11 TVL Male', 'G11 TVL Female', 'G11 SPORTS Male', 'G11 SPORTS Female',
    'G11 ARTS Male', 'G11 ARTS Female', 'G12 ACAD ABM Male', 'G12 ACAD ABM Female',
    'G12 ACAD HUMSS Male', 'G12 ACAD HUMSS Female', 'G12 ACAD STEM Male', 'G12 ACAD STEM Female',
    'G12 ACAD GAS Male', 'G12 ACAD GAS Female', 'G12 ACAD PBM Male', 'G12 ACAD PBM Female',
    'G12 TVL Male', 'G12 TVL Female', 'G12 SPORTS Male', 'G12 SPORTS Female',
    'G12 ARTS Male', 'G12 ARTS Female'
]

df[enrollment_columns] = df[enrollment_columns].apply(pd.to_numeric, errors='coerce').fillna(0)

# Total schools
total_schools = df.shape[0]

# Export the value
def get_total_schools():
    return total_schools

def get_school_crowding_figure(df):
    enrollee_columns = [
        'K Male', 'K Female', 'G1 Male', 'G1 Female', 'G2 Male', 'G2 Female',
        'G3 Male', 'G3 Female', 'G4 Male', 'G4 Female', 'G5 Male', 'G5 Female',
        'G6 Male', 'G6 Female', 'Elem NG Male', 'Elem NG Female', 'G7 Male', 'G7 Female',
        'G8 Male', 'G8 Female', 'G9 Male', 'G9 Female', 'G10 Male', 'G10 Female',
        'JHS NG Male', 'JHS NG Female', 'G11 ACAD ABM Male', 'G11 ACAD ABM Female',
        'G11 ACAD HUMSS Male', 'G11 ACAD HUMSS Female', 'G11 ACAD STEM Male', 'G11 ACAD STEM Female',
        'G11 ACAD GAS Male', 'G11 ACAD GAS Female', 'G11 ACAD PBM Male', 'G11 ACAD PBM Female',
        'G11 TVL Male', 'G11 TVL Female', 'G11 SPORTS Male', 'G11 SPORTS Female',
        'G11 ARTS Male', 'G11 ARTS Female', 'G12 ACAD ABM Male', 'G12 ACAD ABM Female',
        'G12 ACAD HUMSS Male', 'G12 ACAD HUMSS Female', 'G12 ACAD STEM Male', 'G12 ACAD STEM Female',
        'G12 ACAD GAS Male', 'G12 ACAD GAS Female', 'G12 ACAD PBM Male', 'G12 ACAD PBM Female',
        'G12 TVL Male', 'G12 TVL Female', 'G12 SPORTS Male', 'G12 SPORTS Female',
        'G12 ARTS Male', 'G12 ARTS Female'
    ]

    df[enrollee_columns] = df[enrollee_columns].apply(pd.to_numeric, errors='coerce').fillna(0)
    df['Total Enrollees'] = df[enrollee_columns].sum(axis=1)

    region_summary = df.groupby('Region').agg({
        'Total Enrollees': 'sum',
        'BEIS School ID': 'nunique'
    }).reset_index()

    region_summary.rename(columns={'BEIS School ID': 'Number of Schools'}, inplace=True)
    region_summary['Enrollees per School'] = (region_summary['Number of Schools'] / region_summary['Total Enrollees']) * 100
    region_summary = region_summary.sort_values(by='Enrollees per School', ascending=False).reset_index(drop=True)

    colors = ['#084683' if i == 0 or i == len(region_summary) - 1 else '#0174DF' for i in range(len(region_summary))]

    fig = go.Figure(data=[
        go.Bar(
            name='Enrollees per School',
            x=region_summary['Region'],
            y=region_summary['Enrollees per School'],
            marker_color=colors,
            text=region_summary['Enrollees per School'].round(2),
            textposition='outside'
        )
    ])

    fig.update_layout(
        height=600,
        title=dict(
            text='Measures of School Crowding per Region',
            font=dict(size=15)
        ),
        xaxis_title='Region',
        yaxis=dict(
            title='Percentage (%)',
            range=[0, region_summary['Enrollees per School'].max() * 1.1]
        ),
        barmode='group',
        legend=dict(title='Metric'),
        xaxis_tickangle=-45,
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        margin=dict(b=200),
        annotations=[
            dict(
                text="Normal crowding across regions will be reached after <b>n years</b>",
                xref="paper", yref="paper",
                x=1, y=-0.6,
                showarrow=False,
                font=dict(size=18, color="#084683"),
                xanchor='right'
            ),
            dict(
                text="Student Population Heatmap by Region and Strand",
                xref="paper", yref="paper",
                x=-0.1, y=-0.8,
                showarrow=False,
                font=dict(size=24, color="#DE082C"),
                xanchor='left'
            )
        ]
    )

    return fig

def get_subclassification_bubble_chart(df):
    # Count subclassifications per region
    region_subclassification_counts = defaultdict(lambda: defaultdict(int))
    for _, row in df.iterrows():
        region = row['Region']
        subclassification = row['School Subclassification']
        region_subclassification_counts[region][subclassification] += 1

    subclassification_data = []
    for region, subclassifications in region_subclassification_counts.items():
        for subclassification, count in subclassifications.items():
            subclassification_data.append({
                'Region': region,
                'School Subclassification': subclassification,
                'Count': count
            })
    subclassification_df = pd.DataFrame(subclassification_data)

    enrollee_columns = [col for col in df.columns if 'Male' in col or 'Female' in col]
    df['Total Enrollees'] = df[enrollee_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)

    region_summary = df.groupby('Region').agg({
        'Total Enrollees': 'sum',
        'BEIS School ID': 'nunique'
    }).reset_index()

    region_summary.rename(columns={'BEIS School ID': 'Number of Schools'}, inplace=True)
    region_summary['Schools per Enrollee'] = (region_summary['Number of Schools'] / region_summary['Total Enrollees']) * 100

    merged_df = pd.merge(subclassification_df, region_summary, on='Region')

    fig = px.scatter(
        merged_df,
        x='Schools per Enrollee',
        y='Count',
        size='Count',
        size_max=60,
        color='School Subclassification',
        hover_name='Region',
        title='Comparison of Schools per Enrollee and School Subclassification Counts',
        labels={'Schools per Enrollee': 'Schools per Enrollee (%)', 'Count': 'School Subclassification Count'},
        template='plotly',
        color_discrete_sequence=['#084683', '#DE082C', '#F2EC1A', '#D9D9D9']
    )

    fig.update_layout(
        title_font_size=15,
        margin=dict(b=200),
        height=700,
    )

    return fig

def add_annotation(fig):
    # Hardcoded custom text annotation
    annotation_text = "<span style='color:#B03B60; font-weight:bold;'>Enrollment Analytics:</span><br>" \
                      "Expect a <b>n%</b> increase in this region next year.<br>" \
                      "Projected Students for Year n+1: <b>28,057,844</b><br>" \
                      "<b>{region}</b> has the highest amount of enrollees for 2024"

    fig.add_annotation(
        text=annotation_text,
        xref="paper", yref="paper",
        x=0, y=-0.6,  # Adjust the y-value to place the annotation below the chart
        showarrow=False,
        align="left",
        font=dict(size=18),
        xanchor="left",
    )
    return fig

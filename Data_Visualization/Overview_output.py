import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go
import plotly.express as px
import json
import os

# ——— Pie Chart: Total Enrollees by Level ———
def pie_chart_total_enrollees(df: pd.DataFrame) -> go.Figure:
    """
    Builds a donut‐style pie chart showing total enrollees
    broken down by Kindergarten, ELEM, JHS, and SHS levels.
    Expects a DataFrame with columns matching the combined_levels dict.
    """
    # Define which columns belong to each level
    combined_levels = {
        'Kindergarten': ['K Male', 'K Female'],
        'ELEM': [
            'G1 Male', 'G1 Female', 'G2 Male', 'G2 Female',
            'G3 Male', 'G3 Female', 'G4 Male', 'G4 Female',
            'G5 Male', 'G5 Female', 'G6 Male', 'G6 Female',
            'Elem NG Male', 'Elem NG Female'
        ],
        'JHS': [
            'G7 Male', 'G7 Female', 'G8 Male', 'G8 Female',
            'G9 Male', 'G9 Female', 'G10 Male', 'G10 Female',
            'JHS NG Male', 'JHS NG Female'
        ],
        'SHS': [
            'G11 ACAD ABM Male', 'G11 ACAD ABM Female',
            'G11 ACAD HUMSS Male', 'G11 ACAD HUMSS Female',
            'G11 ACAD STEM Male', 'G11 ACAD STEM Female',
            'G11 ACAD GAS Male', 'G11 ACAD GAS Female',
            'G11 ACAD PBM Male', 'G11 ACAD PBM Female',
            'G11 TVL Male', 'G11 TVL Female',
            'G11 SPORTS Male', 'G11 SPORTS Female',
            'G11 ARTS Male', 'G11 ARTS Female',
            'G12 ACAD ABM Male', 'G12 ACAD ABM Female',
            'G12 ACAD HUMSS Male', 'G12 ACAD HUMSS Female',
            'G12 ACAD STEM Male', 'G12 ACAD STEM Female',
            'G12 ACAD GAS Male', 'G12 ACAD GAS Female',
            'G12 ACAD PBM Male', 'G12 ACAD PBM Female',
            'G12 TVL Male', 'G12 TVL Female',
            'G12 SPORTS Male', 'G12 SPORTS Female',
            'G12 ARTS Male', 'G12 ARTS Female'
        ]
    }

    # Ensure numeric and fill gaps
    for cols in combined_levels.values():
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce').fillna(0)

    # Compute sums per level
    combined_totals = {
        level: df[cols].sum().sum()
        for level, cols in combined_levels.items()
    }
    total_all = sum(combined_totals.values())

    # Build the figure
    fig = go.Figure(
        data=[go.Pie(
            labels=list(combined_totals.keys()),
            values=list(combined_totals.values()),
            hole=0.55,
            textinfo='label+percent',
            marker=dict(colors=['#0174DF','#0154A2','#DE082C','#F2EC1A'])
        )]
    )

    fig.update_layout(
        title={
            'text': (
                "Total Enrollees by Level"
                f"<br><sub>Total: {total_all:,}</sub>"
            ),
            'x': 0.5,                   # center
            'y': 1,                     # top of plot
            'xanchor': 'center',
            'yanchor': 'bottom',
            'pad': {'t': 20}            # 20px padding above title
        },
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.1,
            xanchor="center", x=0.5, font=dict(size=12)
        ),
        height=400,
        margin=dict(t=80, b=40, l=30, r=30)  # 80px top margin
    )

    return fig


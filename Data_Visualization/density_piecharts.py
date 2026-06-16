import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64
import matplotlib.pyplot as plt

def public_pie_chart(df):
    public_schools = df[df['Sector'].isin(['Public', 'SUCsLUCs'])]

    combined_levels = {
        'Kindergarten': ['K Male', 'K Female'],
        'ELEM': ['G1 Male', 'G1 Female', 'G2 Male', 'G2 Female', 'G3 Male', 'G3 Female', 'G4 Male', 'G4 Female', 'G5 Male', 'G5 Female', 'G6 Male', 'G6 Female', 'Elem NG Male', 'Elem NG Female'],
        'JHS': ['G7 Male', 'G7 Female', 'G8 Male', 'G8 Female', 'G9 Male', 'G9 Female', 'G10 Male', 'G10 Female', 'JHS NG Male', 'JHS NG Female'],
        'SHS': ['G11 ACAD ABM Male', 'G11 ACAD ABM Female', 'G11 ACAD HUMSS Male', 'G11 ACAD HUMSS Female', 'G11 ACAD STEM Male', 'G11 ACAD STEM Female', 'G11 ACAD GAS Male', 'G11 ACAD GAS Female', 'G11 ACAD PBM Male', 'G11 ACAD PBM Female', 'G11 TVL Male', 'G11 TVL Female', 'G11 SPORTS Male', 'G11 SPORTS Female', 'G11 ARTS Male', 'G11 ARTS Female', 'G12 ACAD ABM Male', 'G12 ACAD ABM Female', 'G12 ACAD HUMSS Male', 'G12 ACAD HUMSS Female', 'G12 ACAD STEM Male', 'G12 ACAD STEM Female', 'G12 ACAD GAS Male', 'G12 ACAD GAS Female', 'G12 ACAD PBM Male', 'G12 ACAD PBM Female', 'G12 TVL Male', 'G12 TVL Female', 'G12 SPORTS Male', 'G12 SPORTS Female', 'G12 ARTS Male', 'G12 ARTS Female']
    }

    all_enrollee_columns = [col for level_cols in combined_levels.values() for col in level_cols]
    public_schools[all_enrollee_columns] = public_schools[all_enrollee_columns].apply(pd.to_numeric, errors='coerce').fillna(0)
    public_schools['Total Enrollees'] = public_schools[all_enrollee_columns].sum(axis=1)

    level_enrollment = {}
    for level, columns in combined_levels.items():
        level_enrollment[level] = public_schools[columns].sum().sum()

    level_enrollment_df = pd.DataFrame(level_enrollment.items(), columns=['Level', 'Total Enrollment'])
    level_enrollment_df['Percentage'] = (level_enrollment_df['Total Enrollment'] / level_enrollment_df['Total Enrollment'].sum()) * 100

    custom_colors = ['#0174DF', '#0154A2', '#F2EC1A', '#DE082C']

    labels_trace = go.Pie(
        labels=level_enrollment_df['Level'], 
        values=level_enrollment_df['Percentage'], 
        hole=0,
        sort=False,
        textinfo='label',  
        textposition='outside',  
        marker=dict(colors=custom_colors),
	domain={'x': [0, 1], 'y': [0, 1]},
        showlegend=False 
    )

    percentages_trace = go.Pie(
        labels=level_enrollment_df['Level'], 
        values=level_enrollment_df['Percentage'], 
        hole=0,
        sort=False,
        textinfo='percent',  
        textposition='inside',  
        insidetextfont=dict(color="black"), 
        marker=dict(colors=custom_colors),
        domain={'x': [0, 1], 'y': [0, 1]},
        showlegend=False  
    )

    fig = go.Figure(data=[labels_trace, percentages_trace])
    
    fig.update_layout(title="", height=390, legend_title_text="Grade Levels", margin=dict(t=0, b=0, l=0, r=0), legend=dict(
        title="Grade Levels",  
        borderwidth=1,  
        bordercolor="lightgray",  
        traceorder="normal",  
        orientation="h",  
        y=-0.2,  
        yanchor="bottom",  
        x=0.5,  
        xanchor="center",
        font=dict(size=10)
    ))
    return fig


def private_pie_chart(df):
    private_schools = df[df['Sector'].isin(['Private', 'PSO'])]

    combined_levels = {
        'Kindergarten': ['K Male', 'K Female'],
        'ELEM': ['G1 Male', 'G1 Female', 'G2 Male', 'G2 Female', 'G3 Male', 'G3 Female',
                 'G4 Male', 'G4 Female', 'G5 Male', 'G5 Female', 'G6 Male', 'G6 Female',
                 'Elem NG Male', 'Elem NG Female'],
        'JHS': ['G7 Male', 'G7 Female', 'G8 Male', 'G8 Female', 'G9 Male', 'G9 Female',
                'G10 Male', 'G10 Female', 'JHS NG Male', 'JHS NG Female'],
        'SHS': ['G11 ACAD ABM Male', 'G11 ACAD ABM Female', 'G11 ACAD HUMSS Male', 'G11 ACAD HUMSS Female',
                'G11 ACAD STEM Male', 'G11 ACAD STEM Female', 'G11 ACAD GAS Male', 'G11 ACAD GAS Female',
                'G11 ACAD PBM Male', 'G11 ACAD PBM Female', 'G11 TVL Male', 'G11 TVL Female',
                'G11 SPORTS Male', 'G11 SPORTS Female', 'G11 ARTS Male', 'G11 ARTS Female',
                'G12 ACAD ABM Male', 'G12 ACAD ABM Female', 'G12 ACAD HUMSS Male', 'G12 ACAD HUMSS Female',
                'G12 ACAD STEM Male', 'G12 ACAD STEM Female', 'G12 ACAD GAS Male', 'G12 ACAD GAS Female',
                'G12 ACAD PBM Male', 'G12 ACAD PBM Female', 'G12 TVL Male', 'G12 TVL Female',
                'G12 SPORTS Male', 'G12 SPORTS Female', 'G12 ARTS Male', 'G12 ARTS Female']
    }

    all_enrollee_columns = [col for cols in combined_levels.values() for col in cols]
    private_schools[all_enrollee_columns] = private_schools[all_enrollee_columns].apply(pd.to_numeric, errors='coerce').fillna(0)

    level_enrollment = {}
    for level, columns in combined_levels.items():
        level_enrollment[level] = private_schools[columns].sum().sum()

    level_enrollment_df = pd.DataFrame(level_enrollment.items(), columns=['Level', 'Total Enrollment'])
    level_enrollment_df['Percentage'] = (level_enrollment_df['Total Enrollment'] / level_enrollment_df['Total Enrollment'].sum()) * 100

    custom_colors = ['#0174DF', '#0154A2', '#F2EC1A', '#DE082C']

    labels_trace = go.Pie(
        labels=level_enrollment_df['Level'], 
        values=level_enrollment_df['Percentage'], 
        hole=0,
        sort=False,
        textinfo='label',
        textposition='outside',
        marker=dict(colors=custom_colors),
        domain={'x': [0, 1], 'y': [0, 1]},
        showlegend=False
    )

    percentages_trace = go.Pie(
        labels=level_enrollment_df['Level'], 
        values=level_enrollment_df['Percentage'], 
        hole=0,
        sort=False,
        textinfo='percent',
        textposition='inside',
        insidetextfont=dict(color="black"),
        marker=dict(colors=custom_colors),
        domain={'x': [0, 1], 'y': [0, 1]},
        showlegend=False
    )

    fig = go.Figure(data=[labels_trace, percentages_trace])

    fig.update_layout(title="", height=600, legend_title_text="Grade Levels", margin=dict(t=0, b=0, l=0, r=0), legend=dict(
        title="Grade Levels",  
        borderwidth=1,  
        bordercolor="lightgray", 
        traceorder="normal", 
        orientation="h",  
        y=-0.2,  
        yanchor="bottom",  
        x=0.5,  
        xanchor="center",  
        font=dict(size=10)
    ))

    return fig

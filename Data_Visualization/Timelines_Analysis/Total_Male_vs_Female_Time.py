import pandas as pd
import plotly.express as px
import os
import re

# Automatically reads cleaned file
def load_and_process_data(directory):
    data = []
    pattern = re.compile(r'CLEANED_SY(\d{4})_Enrollment\.csv')

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            year = int(match.group(1))
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)

            # Separate male and female enrollment columns
            male_columns = [col for col in df.columns if col.endswith('Male')]
            female_columns = [col for col in df.columns if col.endswith('Female')]

            total_male = df[male_columns].sum().sum()
            total_female = df[female_columns].sum().sum()

            data.append({
                'Year': year,
                'Total Male Enrollees': total_male,
                'Total Female Enrollees': total_female
            })

    return pd.DataFrame(data)

# Function to plot enrollment trends
def plot_enrollment_trend_by_gender(data):
    data = data.sort_values(by='Year')

    melted = data.melt(
        id_vars='Year',
        value_vars=['Total Male Enrollees', 'Total Female Enrollees'],
        var_name='Gender',
        value_name='Total Enrollees'
    )

    fig = px.line(
        melted,
        x='Year',
        y='Total Enrollees',
        color='Gender',
        title='Total Male vs Female Enrollees by Year',
        markers=True,
        color_discrete_map={
            'Total Male Enrollees': '#084683',  # blue
            'Total Female Enrollees': '#DE082C'  # red
        }
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=10, symbol="circle")
    )

    fig.update_layout(
        title_x=0.5,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Monserrat', size=14, color='#333'),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.4,
            xanchor='center',
            x=0.5,
            font=dict(size=12)
        ),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(
        dtick=1,
        tickformat='.0f',
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    )

    return fig

# Set the folder containing the cleaned enrollment files
csv_folder = 'CSV Files'

# Load and process data
enrollment_data = load_and_process_data(csv_folder)

# Plot the dual line chart
enrollment_trend_by_gender = plot_enrollment_trend_by_gender(enrollment_data)

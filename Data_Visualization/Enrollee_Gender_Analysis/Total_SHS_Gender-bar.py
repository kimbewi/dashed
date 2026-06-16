import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# based on figma dont use nalang

# Load dataset
df = pd.read_csv("CSV Files/CLEANED_SY2023_Enrollment.csv")

# Melt columns to long format
melted_df = df.melt(id_vars=["Region"], var_name="Descriptor", value_name="Enrollees")

# Extract Grade Level, Strand, and Gender
extracted = melted_df['Descriptor'].str.extract(r'^(G11|G12)\s*([A-Za-z\s]*)\s+(Male|Female)$')

# Assign extracted values to new columns
melted_df['Grade Level'] = extracted[0].str.replace('G', '')  # Remove the 'G' prefix
melted_df['Strand'] = extracted[1].str.strip()  # Remove extra spaces
melted_df['Gender'] = extracted[2]

# Drop rows where the pattern didn't match
melted_df.dropna(subset=['Grade Level', 'Strand', 'Gender'], inplace=True)

# Ensure numeric
melted_df['Enrollees'] = pd.to_numeric(melted_df['Enrollees'], errors='coerce').fillna(0)

# Group by relevant fields
grouped = melted_df.groupby(['Region', 'Grade Level', 'Strand', 'Gender'], as_index=False)['Enrollees'].sum()

# Get unique values
regions = sorted(grouped['Region'].unique())
regions_with_all = ['All'] + regions
grade_levels = ['11', '12']

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[
    "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
])

# Layout
app.layout = html.Div([
    html.H2("Male and Female Enrollees per Strand (Grades 11 & 12)", className="text-center mt-4"),

    html.Div([
        html.Div([
            html.Label("Select Region:"),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': region, 'value': region} for region in regions_with_all],
                value='All',
                clearable=False,
            )
        ], className="me-4", style={'width': '45%'}),

        html.Div([
            html.Label("Select Grade Level:"),
            dcc.Dropdown(
                id='grade-dropdown',
                options=[{'label': f'Grade {g}', 'value': g} for g in grade_levels],
                value='11',
                clearable=False,
            )
        ], style={'width': '45%'}),
    ], className="d-flex justify-content-center mt-3"),

    html.Div([
        dcc.Graph(id='bar-chart')
    ], className="mt-4 px-4")
])

# Callback
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('grade-dropdown', 'value')]
)
def update_bar_chart(selected_region, selected_grade):
    if selected_region == 'All':
        # Filter and aggregate
        filtered = grouped[grouped['Grade Level'] == selected_grade]
        aggregated = filtered.groupby(['Strand', 'Gender'], as_index=False)['Enrollees'].sum()

        # Compute total per strand
        total_per_strand = aggregated.groupby('Strand')['Enrollees'].transform('sum')
        aggregated['Percentage'] = (aggregated['Enrollees'] / total_per_strand) * 100

        # Add combined label text for each bar segment
        aggregated['Label'] = aggregated.apply(
            lambda row: f"{int(row['Enrollees']):,} ({row['Percentage']:.1f}%)", axis=1
        )

        # Create 100% stacked bar chart
        fig = px.bar(
            aggregated,
            x='Percentage',
            y='Strand',
            color='Gender',
            orientation='h',
            barmode='stack',
            text='Label',
            title=f"Gender Distribution by Strand (All Regions) - Grade {selected_grade}",
            labels={'Percentage': 'Percentage of Students'},
            color_discrete_map={'Male': '#084683', 'Female': '#DE082C'}
        )

        # Calculate total enrollees and append to chart title
        total_all = int(aggregated['Enrollees'].sum())
        fig.update_layout(
            title={
                'text': f"Gender Distribution by Strand (All Regions) - Grade {selected_grade}<br><sub>Total Enrollees: {total_all:,}</sub>",
                'x': 0.5
            },
            xaxis=dict(
                title='Percentage',
                ticksuffix='%',
                range=[0, 100]
            ),
            yaxis_title='Strand',
            height=600,
            legend_title='Gender',
            margin=dict(l=100, r=40, t=80, b=60)
        )

        # Position labels inside bars
        fig.update_traces(textposition='inside', insidetextanchor='middle')
    else:
        # Filter for region and grade
        filtered = grouped[
            (grouped['Region'] == selected_region) &
            (grouped['Grade Level'] == selected_grade)
        ]

        fig = px.bar(
            filtered,
            x='Enrollees',
            y='Strand',
            color='Gender',
            barmode='group',
            orientation='h',
            title=f"Enrollees in Region {selected_region} - Grade {selected_grade}",
            labels={'Enrollees': 'Number of Students'},
            color_discrete_map={'Male': '#084683', 'Female': '#DE082C'},
            text='Enrollees'
        )

        fig.update_layout(
            xaxis_title='Number of Students',
            yaxis_title='Strand',
            height=600,
            legend_title='Gender',
            margin=dict(l=100, r=40, t=60, b=60)
        )

        fig.update_traces(textposition='auto')

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

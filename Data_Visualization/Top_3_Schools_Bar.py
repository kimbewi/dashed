import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# based on figma dont add yet
# Load the dataset (change later to let user select dataset!!)
df = pd.read_csv('CSV Files/CLEANED_SY2023_Enrollment.csv')  # Adjust path as needed

# Grade levels and corresponding columns
grade_levels = {
    'Kinder': ('K Male', 'K Female'),
    'Grade 1': ('G1 Male', 'G1 Female'),
    'Grade 2': ('G2 Male', 'G2 Female'),
    'Grade 3': ('G3 Male', 'G3 Female'),
    'Grade 4': ('G4 Male', 'G4 Female'),
    'Grade 5': ('G5 Male', 'G5 Female'),
    'Grade 6': ('G6 Male', 'G6 Female'),
    'Grade 7': ('G7 Male', 'G7 Female'),
    'Grade 8': ('G8 Male', 'G8 Female'),
    'Grade 9': ('G9 Male', 'G9 Female'),
    'Grade 10': ('G10 Male', 'G10 Female'),
    'Grade 11': ('G11 TVL Male', 'G11 TVL Female'),
    'Grade 12': ('G12 TVL Male', 'G12 TVL Female')
}

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"])
app.title = 'DepEd Enrollment by Region'

app.layout = html.Div([
    html.H2("DepEd Enrollment by Region per Grade Level", className="text-center my-4"),
    
    html.Div([
        dcc.Dropdown(
            id='grade-dropdown',
            options=[{'label': level, 
                      'value': level} for level in grade_levels.keys()],
            value='Grade 1', # Default value
            clearable=False, # Dropdown cannot be cleared
            className='mb-4' # Bootstrap class for margin
        ),
    ], className="container"), # Bootstrap class for centering

    dcc.Graph(id='bar-chart') # Bar chart for total enrollees
])

@app.callback(
    Output('bar-chart', 'figure'),
    Input('grade-dropdown', 'value')
)

# Callback function to update the bar chart based on selected grade
def update_bar_chart(selected_grade):
    male_col, female_col = grade_levels[selected_grade]
    df_grouped = df.groupby('Region')[[male_col, female_col]].sum()
    df_grouped['Total'] = df_grouped[male_col] + df_grouped[female_col]

    # Sort by Total in descending order
    df_grouped = df_grouped.sort_values(by='Total', ascending=False)

    # Identify top 3 regions
    top_3_regions = df_grouped.head(3).index

    # Assign color categories
    df_grouped['Color'] = ['Top Region' if region in top_3_regions else 'Other' for region in df_grouped.index]

    # Plotly bar chart
    fig = px.bar(
        df_grouped.reset_index(),
        x='Region',
        y='Total',
        color='Color', # Color by Top Region or Other
        color_discrete_map={'Top Region': '#f08080', 'Other': '#a8ddb5'}, # Adjust colors as needed
        text='Total' # Display total enrollees on bars
    )

    fig.update_traces(texttemplate='%{text:,}', # Format text with commas
                      textposition='outside') # Position text outside the bar
    fig.update_layout(
        title=f"Total Enrollees in {selected_grade} per Region (Descending Order)",
        xaxis_title="Regions",
        yaxis_title="Total Enrollees",
        xaxis_tickangle=-45, # Rotate x-axis labels for better readability
        plot_bgcolor='#f4f4f4', # Background color
        yaxis=dict(showgrid=True, gridcolor='#cccccc'), # Grid lines
        font=dict(color='#333333'), # Font color
        legend_title=None, # Legend title
        margin=dict(t=80, b=80) # Margin settings
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

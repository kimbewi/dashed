import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Load your dataset
combined_population_df = pd.read_csv('CSV Files/combined_population_2023.csv')

# Define available grade levels
grade_levels = ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12']

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"])

# Define the layout
app.layout = html.Div([
    html.H2("Student Population Heatmap by Grade", className="text-center mt-4"),

    html.Div([
        dcc.Dropdown(
            id='grade-dropdown', # Dropdown for selecting grade level
            options=[{'label': grade, # Label for each option
                      'value': grade}  # Value for each option
                      for grade in grade_levels], # List of options
            value='G11', # Default value
            clearable=False, # Disable clearing of selection
            style={'width': '50%'} # styles of the dropdown
        ),
    ], className="d-flex justify-content-center mt-3"), # Centers the dropdown

    html.Div([
        dcc.Graph(id='heatmap', style={'height': '800px'}) # Heatmap graph style
    ], className="mt-4 px-4"),

    html.H4("Total Enrollees per Grade Level", className="text-center mt-5"), # Title for bar chart

    html.Div([
        dcc.Graph(id='bar-chart') # Bar chart for total enrollees per grade level
    ], className="mt-3 px-4")
])

# Define the heatmap callback
@app.callback(
    Output('heatmap', 'figure'), # Output for the heatmap
    Input('grade-dropdown', 'value') # Input for the selected grade level
)

# Callback function to update the heatmap based on selected grade
def update_heatmap(selected_grade):
    # Define mapping of grade levels to corresponding columns
    grade_columns = [col for col in combined_population_df.columns if f'{selected_grade} ' in col and 'Total' in col]

    # Check if there are any columns for the selected grade
    if not grade_columns:
        return px.imshow([[0]], labels=dict(x="Strand", y="Region", color="Students"),
                         title=f"No data available for Grade {selected_grade}")

    # Melt the DataFrame to long format for heatmap
    # This will create a DataFrame with 'Region', 'Strand', and 'Total Students' columns
    melted_df = combined_population_df.melt(
        id_vars=['Region'],
        value_vars=grade_columns,
        var_name="Strand",
        value_name="Total Students"
    )

    # Extract the strand name from the column names
    melted_df['Strand'] = melted_df['Strand'].str.extract(r'(\b[A-Za-z]+\b)')

    # Group by Region and Strand, summing the total students
    aggregated_df = melted_df.groupby(['Region', 'Strand'], as_index=False).sum()

    # Pivot the DataFrame to create a heatmap format
    # This will create a DataFrame with regions as rows, strands as columns, and total students as values
    heatmap_data = aggregated_df.pivot(index='Region', columns='Strand', values='Total Students').fillna(0)

    # Sort the DataFrame by Region
    fig = px.imshow(
        heatmap_data, # Create the heatmap
        labels=dict(x="Strand", y="Region", color="Students"), # Labels for axes and color
        x=heatmap_data.columns, # X-axis labels (Strands)
        y=heatmap_data.index, # Y-axis labels (Regions)
        color_continuous_scale="viridis", # Color scale for the heatmap
        text_auto=True, # Auto text for values
        aspect="auto" # Maintain aspect ratio
    )

    # Update layout of the heatmap
    fig.update_layout(
        title=f"Student Population by Region and Strand (Grade {selected_grade})", # Title of the heatmap
        xaxis_title="Strand", # X-axis title
        yaxis_title="Region", # Y-axis title
        autosize=False, # Set fixed size for the heatmap
        width=1000, # Width of the heatmap
        height=800, # Height of the heatmap
        margin=dict(l=100, r=50, t=100, b=100), # Margin settings
        font=dict(size=12) # Font size for the text
    )
    fig.update_xaxes(tickangle=45) # Rotate x-axis labels for better readability

    return fig

# Callback for bar chart of total enrollees per grade
@app.callback(
    Output('bar-chart', 'figure'), # Bar chart output
    Input('grade-dropdown', 'value') # Input for the selected grade level (not used in this callback, but included for consistency with the heatmap callback
)
def update_bar_chart(selected_grade):
    # Define mapping of grade levels to corresponding columns
    grade_column_map = {
        'K': ['K Total'],
        'G1': ['G1 Total'],
        'G2': ['G2 Total'],
        'G3': ['G3 Total'],
        'G4': ['G4 Total'],
        'G5': ['G5 Total'],
        'G6': ['G6 Total'],
        'G7': ['G7 Total'],
        'G8': ['G8 Total'],
        'G9': ['G9 Total'],
        'G10': ['G10 Total'],
        'G11': [col for col in combined_population_df.columns if col.startswith('G11')],
        'G12': [col for col in combined_population_df.columns if col.startswith('G12')],
    }

    # Sum population for each grade level
    grade_totals = []
    for grade in grade_levels:
        columns = grade_column_map.get(grade, [])
        total = combined_population_df[columns].sum().sum() if columns else 0
        grade_totals.append(total)

    # Create a bar chart for total enrollees per grade level
    fig = px.bar(
        x=grade_levels, # X-axis values (Grade Levels)
        y=grade_totals, # Y-axis values (Total Enrollees)
        labels={'x': 'Grade Level', 'y': 'Total Enrollees'}, # Labels for axes
        title='Total Enrollees per Grade Level', # Title of the bar chart
        #text=grade_totals, # Text on bars disabled for now for cleanliness
        color=grade_levels, # Color by grade levels
        height=400, # Height of the bar chart
        width=600, # Width of the bar chart
        color_discrete_sequence=px.colors.qualitative.Set2  # Color sequence for the bars
    )
    fig.update_traces(
        width=0.9, # Bar width
        marker_color='skyblue') # Bar color
    
    fig.update_layout(xaxis_tickangle=-45, showlegend=False) # Rotate x-axis labels for better readability

    return fig


# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)

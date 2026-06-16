import pandas as pd
import plotly.graph_objects as go

# Load the dataset
df = pd.read_csv('CSV Files/CLEANED_SY2023_Enrollment.csv')  # Replace with your file path

# List of columns to sum for total enrollees
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

# Calculate total enrollees per row
df['Total Enrollees'] = df[enrollee_columns].sum(axis=1)

# Group by region and aggregate
region_summary = df.groupby('Region').agg({
    'Total Enrollees': 'sum',
    'BEIS School ID': 'nunique'
}).reset_index()

# Rename column
region_summary.rename(columns={'BEIS School ID': 'Number of Schools'}, inplace=True)

# Calculate crowding metric!!
# calculation for school per enrolleee
region_summary['Enrollees per School'] = (region_summary['Number of Schools'] / region_summary['Total Enrollees']) * 100

# Sorts by School per Enrollee
region_summary = region_summary.sort_values(by='Enrollees per School', ascending=False).reset_index(drop=True)

# Generates bar colors
colors = []
for idx in range(len(region_summary)):
    if idx == 0 or idx == len(region_summary) - 1:
        colors.append('green')  # Highest and lowest
    else:
        colors.append('#90ee90')  # Light green for middle values

# Formats each bar of the chart
fig = go.Figure(data=[
    go.Bar(
        name='Enrollees per School', # Bar name
        x=region_summary['Region'], # X-axis values
        y=region_summary['Enrollees per School'], # Y-axis values
        marker_color=colors, # Bar colors
        text=region_summary['Enrollees per School'].round(2), # Text on bars
        textposition='outside'  # Show above the bars
    )
])

# Updates the entire chart
fig.update_layout(
    title='Measures of School Crowding per Region', # Title of the chart
    xaxis_title='Region', # X-axis title
    yaxis_title='Percentage (%)', # Y-axis title
    barmode='group', # Bar mode
    legend=dict(title='Metric'), # Legend title
    xaxis_tickangle=-45, # X-axis tick angle (angle of text on x-axis)
    uniformtext_minsize=8, # Minimum text size
    uniformtext_mode='hide' # Hides text if it doesn't fit
)

# Show the plot
fig.show()

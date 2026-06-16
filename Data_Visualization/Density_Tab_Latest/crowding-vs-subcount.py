import pandas as pd
import plotly.express as px
from collections import defaultdict
import csv

# Load the dataset for school subclassifications
file_name = "CSV Files/CLEANED_SY2023_Enrollment.csv"

# Dictionary to store counts of subclassifications per region
region_subclassification_counts = defaultdict(lambda: defaultdict(int))

# Process the CSV file to count subclassifications per region
with open(file_name, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        region = row['Region']
        subclassification = row['School Subclassification']
        region_subclassification_counts[region][subclassification] += 1

# Convert subclassification counts to a DataFrame
subclassification_data = []
for region, subclassifications in region_subclassification_counts.items():
    for subclassification, count in subclassifications.items():
        subclassification_data.append({
            'Region': region,
            'School Subclassification': subclassification,
            'Count': count
        })

subclassification_df = pd.DataFrame(subclassification_data)

# Load the dataset for "Enrollees per School"
df = pd.read_csv('CSV Files/CLEANED_SY2023_Enrollment.csv')

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

# Calculate crowding metric
region_summary['Schools per Enrollee'] = (region_summary['Number of Schools'] / region_summary['Total Enrollees']) * 100

# Merge the two datasets
merged_df = pd.merge(subclassification_df, region_summary, on='Region')

# Create the bubble chart
fig = px.scatter(
    merged_df,
    x='Schools per Enrollee',
    y='Count',
    size='Count',
    size_max=60,
    color='School Subclassification',
    hover_name='Region',
    title='Comparison of Schools per Enrollee and School Subclassification Counts',
    labels={'School per Enrollee': 'School per Enrollee (%)', 'Count': 'School Subclassification Count'},
    template='plotly'
)

# Show the plot
fig.show()
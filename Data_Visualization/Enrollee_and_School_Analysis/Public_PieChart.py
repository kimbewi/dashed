#Public School PIE CHART

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset (change later to let user select dataset!!)
df = pd.read_csv('CSV Files/CLEANED_SY2023_Enrollment.csv')

# Filter for public schools
public_schools = df[df['Sector'].isin(['Public', 'SUCsLUCs'])]  # Changed to 'Public'

# Ditionary or List of columns to sum for total enrollees
combined_levels = {
    'Kindergarten': [
        'K Male', 'K Female'
    ],
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

# Get a list of all columns to use
all_enrollee_columns = [col for level_cols in combined_levels.values() for col in level_cols]

# Calculate total enrollees per row for public_schools DataFrame
public_schools['Total Enrollees'] = public_schools[all_enrollee_columns].sum(axis=1)

# Calculate enrollment for each combined level
level_enrollment = {}
for level, columns in combined_levels.items():
    level_enrollment[level] = public_schools[columns].sum().sum()  # Sum across all specified columns

# Convert to DataFrame for easier plotting
level_enrollment_df = pd.DataFrame(level_enrollment.items(), columns=['Level', 'Total Enrollment'])

# Calculate percentage distribution
level_enrollment_df['Percentage'] = (level_enrollment_df['Total Enrollment'] / level_enrollment_df['Total Enrollment'].sum()) * 100

# Format Pie Chart 
# Create the pie chart with spacing between slices and legend
plt.figure(figsize=(10, 10))
wedges, labels, autopct_texts = plt.pie(level_enrollment_df['Percentage'], # Data for the pie chart
                                        labels=level_enrollment_df['Level'], # Labels for each slice
                                        autopct='%1.1f%%', # Percentage format
                                        startangle=90, # Start angle for the pie chart
                                        textprops={'fontsize': 10}, # Text properties
                                        wedgeprops={'linewidth': 1, 'edgecolor': 'white'}) # Wedge properties
plt.title('Distribution of Public Schools, SUCs, and LUCs by Enrollees per Grade Levels (Enrollment Percentage)', fontsize=14)
plt.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle

# Add a legend to the side
plt.legend(wedges, # Labels for each slice
           level_enrollment_df['Level'], # Legend labels
           title='Grade Levels', # Title for the legend 
           loc='center left', # Legend location
           bbox_to_anchor=(1, 0.5)) # Legend position

plt.tight_layout() # Adjust layout to make room for the legend
plt.show()
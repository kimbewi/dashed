import pandas as pd
import glob
import os
import re

# Define the path and pattern for the CSV files
folder_path = "CSV Files/"
pattern = os.path.join(folder_path, "CLEANED_SY*_Enrollment.csv")

# Find all matching CSV files
csv_files = glob.glob(pattern)

# Function to calculate total enrollees from a DataFrame
def calculate_total_enrollees(df):
    # Select only columns containing 'Male' or 'Female' (case-insensitive)
    enrollment_columns = df.columns[df.columns.str.contains('Male|Female', case=False, regex=True)]
    return df[enrollment_columns].apply(pd.to_numeric, errors='coerce').sum().sum()

# Loop through each file and calculate totals by year
for file in csv_files:
    # Extract the school year (e.g., "2023" from "SY2023")
    match = re.search(r"SY(\d{4})", file)
    school_year = match.group(1) if match else "Unknown"

    # Load the DataFrame
    df = pd.read_csv(file)

    # Clean Sector values: remove leading/trailing spaces, convert to title case
    df['Sector'] = df['Sector'].astype(str).str.strip().str.title()

    # Filter: private sector (Private or PSO)
    private_pso = df[df['Sector'].str.contains(r'\bPrivate\b|\bPso\b', na=False, regex=True)]

    # Filter: public sector (entries that contain "Public")
    public = df[df['Sector'].str.contains(r'\bPublic\b', na=False, regex=True)]

    # Filter: SUCs/LUCs only (strictly labeled as "SucsLucs")
    sucs_lucs_only = df[df['Sector'].str.fullmatch(r'SucsLucs', case=False, na=False)]

    # Calculate totals
    total_private = calculate_total_enrollees(private_pso)
    total_public = calculate_total_enrollees(public)
    total_sucs_lucs = calculate_total_enrollees(sucs_lucs_only)

    # Final adjusted total for Public + SUCs/LUCs
    adjusted_public_total = total_public + total_sucs_lucs

    # Print results
    print(f"School Year {school_year}:")
    print(f"  Total Enrollees in Private + PSO Schools: {int(total_private):,}")
    #print(f"  Total Enrollees in Public Schools: {int(total_public):,}")
    #print(f"  Total Enrollees in SUCs/LUCs-only Schools: {int(total_sucs_lucs):,}")
    print(f"  Total Enrollees in Public + SUCs/LUCs Schools: {int(adjusted_public_total):,}\n")

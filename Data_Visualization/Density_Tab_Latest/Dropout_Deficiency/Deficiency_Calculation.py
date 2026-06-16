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

# Dictionary to store totals by year
enrollment_totals = {}

# Loop through each file and calculate totals by year
for file in csv_files:
    # Extract the school year (e.g., "2023" from "SY2023")
    match = re.search(r"SY(\d{4})", file)
    school_year = int(match.group(1)) if match else None

    if school_year:
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

        # Store totals in the dictionary
        enrollment_totals[school_year] = {
            "Private + PSO": total_private,
            "Public + SUCs/LUCs": adjusted_public_total
        }

# Calculate year-over-year differences and capped ratios
sorted_years = sorted(enrollment_totals.keys())
for i in range(1, len(sorted_years)):
    current_year = sorted_years[i]
    previous_year = sorted_years[i - 1]

    # Subtraction (difference)
    private_diff = enrollment_totals[current_year]["Private + PSO"] - enrollment_totals[previous_year]["Private + PSO"]
    public_diff = enrollment_totals[current_year]["Public + SUCs/LUCs"] - enrollment_totals[previous_year]["Public + SUCs/LUCs"]

    print(f"\nDifference between {previous_year}-{current_year}:")
    print(f"  Private + PSO: {int(private_diff):,}")
    print(f"  Public + SUCs/LUCs: {int(public_diff):,}")

    # Division (ratio), capped at 1.00
    private_ratio = enrollment_totals[current_year]["Private + PSO"] / enrollment_totals[previous_year]["Private + PSO"]
    public_ratio = enrollment_totals[current_year]["Public + SUCs/LUCs"] / enrollment_totals[previous_year]["Public + SUCs/LUCs"]

    private_ratio = min(1.00, private_ratio)
    public_ratio = min(1.00, public_ratio)

    # Decrease from full (1.00 - ratio)
    private_decrease = 1.00 - private_ratio
    public_decrease = 1.00 - public_ratio

    print(f"\nEnrollment Ratio from {previous_year} to {current_year} (Capped at 1.00):")
    print(f"  Private + PSO: {private_ratio:.4f}")
    print(f"  Public + SUCs/LUCs: {public_ratio:.4f}")

    print(f"\nEnrollment Deficiency Ratio (1 - capped ratio):")
    print(f"  Private + PSO: {private_decrease:.4f}")
    print(f"  Public + SUCs/LUCs: {public_decrease:.4f}\n")

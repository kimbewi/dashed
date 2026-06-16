import pandas as pd
import os
import re

# Directories
input_directory = 'CSV Files'
output_directory = 'CSV Files'
os.makedirs(output_directory, exist_ok=True)

# Pattern to find cleaned CSVs by year
pattern = re.compile(r'CLEANED_SY(\d{4})_Enrollment\.csv')

# Loop through files in input directory
files = os.listdir(input_directory)
matched_files = [f for f in files if pattern.match(f)]

if matched_files:
    for filename in matched_files:
        match = pattern.match(filename)
        school_year = match.group(1)

        input_path = os.path.join(input_directory, filename)
        output_filename = f'combined_population_{school_year}.csv'
        output_path = os.path.join(output_directory, output_filename)

        # Skip if output file already exists
        if os.path.exists(output_path):
            print(f"Skipped existing: {output_filename}")
            continue

        # Read cleaned data
        df = pd.read_csv(input_path)

        # Initialize new DataFrame
        combined_df = df[['Region', 'School Name', 'BEIS School ID', 'Division', 'District']].copy()

        # Grades K–10
        grade_levels = ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10']
        for grade in grade_levels:
            male_col = f'{grade} Male'
            female_col = f'{grade} Female'
            if male_col in df.columns and female_col in df.columns:
                combined_df[f'{grade} Total'] = df[male_col].fillna(0) + df[female_col].fillna(0)

        # Grades 11–12 strands
        strands = ['STEM', 'HUMSS', 'ABM', 'GAS', 'TVL', 'SPORTS', 'ARTS', 'PBM']
        for grade in [11, 12]:
            for strand in strands:
                male_col = f'G{grade} ACAD {strand} Male' if strand in ['STEM', 'HUMSS', 'ABM', 'GAS', 'PBM'] else f'G{grade} {strand} Male'
                female_col = f'G{grade} ACAD {strand} Female' if strand in ['STEM', 'HUMSS', 'ABM', 'GAS', 'PBM'] else f'G{grade} {strand} Female'

                if male_col in df.columns and female_col in df.columns:
                    combined_df[f'G{grade} {strand} Total'] = df[male_col].fillna(0) + df[female_col].fillna(0)

        # Save the combined population file
        combined_df.to_csv(output_path, index=False)
        print(f"Combined population saved: {output_filename}")
else:
    print("No cleaned enrollment files found.")

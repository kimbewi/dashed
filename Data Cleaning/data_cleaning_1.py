import pandas as pd
import os
import re

# Directories
input_directory = '_Raw Excel Files'
output_directory = 'CSV Files'
os.makedirs(output_directory, exist_ok=True)

# Regex to match school year and extract first year
pattern = re.compile(r'SY (\d{4})-\d{4} School Level Data on Official Enrollment.*\.xlsx')

# Loop through all files in the input directory
files = os.listdir(input_directory)
matched_files = [f for f in files if pattern.match(f)]

if matched_files:
    for matched_file in matched_files:
        match = pattern.match(matched_file)
        school_year_start = match.group(1)  # e.g., "2023"

        # Construct cleaned output filename
        cleaned_filename = f'CLEANED_SY{school_year_start}_Enrollment.csv'
        cleaned_file_path = os.path.join(output_directory, cleaned_filename)

        # Skip if this cleaned file already exists
        if os.path.exists(cleaned_file_path):
            print(f"Skipped existing file: {cleaned_filename}")
            continue

        # Proceed with reading and cleaning
        dataset_path = os.path.join(input_directory, matched_file)
        df = pd.read_excel(dataset_path, sheet_name='DB', skiprows=4)

        # Drop unnecessary column
        if 'Street Address' in df.columns:
            df.drop(columns=['Street Address'], inplace=True)

        # Remove duplicates and unwanted rows
        df.drop_duplicates(subset='BEIS School ID', inplace=True)
        df.drop(df[df['Region'].str.contains('PSO', na=False)].index, inplace=True)

        # Clean 'School Name' values
        df['School Name'] = df['School Name'].str.replace(r'\bES\b', 'Elementary School', regex=True)
        df['School Name'] = df['School Name'].str.replace(r'\bHS\b', 'High School', regex=True)

        # Rename specific columns
        columns_to_rename = {
            'G11 ACAD - HUMSS Male': 'G11 ACAD HUMSS Male',
            'G11 ACAD - HUMSS Female': 'G11 ACAD HUMSS Female',
            'G11 ACAD - ABM Male': 'G11 ACAD ABM Male',
            'G11 ACAD - ABM Female': 'G11 ACAD ABM Female',
            'G12 ACAD - HUMSS Male': 'G12 ACAD HUMSS Male',
            'G12 ACAD - HUMSS Female': 'G12 ACAD HUMSS Female',
            'G12 ACAD - ABM Male': 'G12 ACAD ABM Male',
            'G12 ACAD - ABM Female': 'G12 ACAD ABM Female',
        }

        df.rename(columns=columns_to_rename, inplace=True)

        # Save cleaned CSV
        df.to_csv(cleaned_file_path, index=False)
        print(f"Cleaned file saved: {cleaned_filename}")
else:
    print("No matching Excel files found in '_Raw Excel Files'.")

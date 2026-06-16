import csv
from collections import defaultdict

# File name
file_name = "CSV Files/CLEANED_SY2023_Enrollment.csv"

# Dictionary to store counts of subclassifications per region
region_subclassification_counts = defaultdict(lambda: defaultdict(int))

try:
    # Open and read the CSV file
    with open(file_name, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Check if required columns exist
        if 'Region' not in csv_reader.fieldnames or 'School Subclassification' not in csv_reader.fieldnames:
            raise ValueError("The CSV file must contain 'Region' and 'School Subclassification' columns.")
        
        # Process each row in the CSV
        for row in csv_reader:
            region = row['Region']
            subclassification = row['School Subclassification']
            
            # Increment the count for the subclassification in the region
            region_subclassification_counts[region][subclassification] += 1

    # Output the results to the terminal
    print("School Subclassification Counts per Region:")
    for region, subclassifications in region_subclassification_counts.items():
        print(f"\nRegion: {region}")
        for subclassification, count in subclassifications.items():
            print(f"  {subclassification}: {count}")

except FileNotFoundError:
    print(f"Error: The file '{file_name}' was not found.")
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
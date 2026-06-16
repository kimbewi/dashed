import pandas as pd
import glob
import re
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

def forecast_enrollment():
    """Forecasts next year's enrollment using exponential smoothing."""
    
    # Find all relevant CSV files matching the naming pattern
    files = glob.glob("CSV Files/CLEANED_SY*_Enrollment.csv")
    enrollment_data = []

    # Loop through each file and compute total enrollment
    for file in files:
        # Extract the year from the filename using regex
        match = re.search(r"SY(\d{4})", file)
        if match:
            year = int(match.group(1))
            df = pd.read_csv(file)

            # Identify all columns with 'Male' or 'Female' in the name
            enrollment_columns = [col for col in df.columns if "Male" in col or "Female" in col]
            total_enrollment = df[enrollment_columns].sum().sum()

            # Append the year and total enrollment to the list
            enrollment_data.append({
                "Year": year,
                "Total Enrollment": total_enrollment
            })

    # Create a DataFrame and sort by year
    enrollment_df = pd.DataFrame(enrollment_data).sort_values("Year")
    enrollment_series = enrollment_df.set_index("Year")["Total Enrollment"]

    # Apply Simple Exponential Smoothing
    model = SimpleExpSmoothing(enrollment_series, initialization_method="legacy-heuristic")
    fit = model.fit(smoothing_level=0.5)

    # Forecast for the next year
    next_year = enrollment_df["Year"].max() + 1
    forecast = fit.forecast(1).iloc[0]

    # Calculate percentage change from the latest known year
    last_enrollment = enrollment_series.iloc[-1]
    change_percent = ((forecast - last_enrollment) / last_enrollment) * 100

    # Determine direction (increase/decrease)
    direction = "increase" if change_percent > 0 else "decrease"

    # Return all relevant data as a dictionary
    return {
        "next_year": next_year,
        "forecast": forecast,
        "change_percent": change_percent,
        "direction": direction,
        "last_enrollment": last_enrollment
    }

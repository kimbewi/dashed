def private_deficiency_chart():    
    import pandas as pd
    import glob
    import os
    import re
    import plotly.express as px

    # Add this as dropdown option
    # title of dropdown: Total 

    # Define the path and pattern for the CSV files
    folder_path = "CSV Files/"
    pattern = os.path.join(folder_path, "CLEANED_SY*_Enrollment.csv")

    # Find all matching CSV files
    csv_files = glob.glob(pattern)

    # Function to calculate total enrollees from a DataFrame
    def calculate_total_enrollees(df):
        enrollment_columns = df.columns[df.columns.str.contains('Male|Female', case=False, regex=True)]
        return df[enrollment_columns].apply(pd.to_numeric, errors='coerce').sum().sum()

    # Dictionary to store totals by year
    enrollment_totals = {}

    # Loop through each file and calculate totals by year
    for file in csv_files:
        match = re.search(r"SY(\d{4})", file)
        school_year = int(match.group(1)) if match else None

        if school_year:
            df = pd.read_csv(file)
            df['Sector'] = df['Sector'].astype(str).str.strip().str.title()

            private_pso = df[df['Sector'].str.contains(r'\bPrivate\b|\bPso\b', na=False, regex=True)]
            public = df[df['Sector'].str.contains(r'\bPublic\b', na=False, regex=True)]
            sucs_lucs_only = df[df['Sector'].str.fullmatch(r'SucsLucs', case=False, na=False)]

            total_private = calculate_total_enrollees(private_pso)
            total_public = calculate_total_enrollees(public)
            total_sucs_lucs = calculate_total_enrollees(sucs_lucs_only)

            adjusted_public_total = total_public + total_sucs_lucs

            enrollment_totals[school_year] = {
                "Private + PSO": total_private,
                "Public + SUCs/LUCs": adjusted_public_total
            }

    # Calculate year-over-year deficiency ratios
    sorted_years = sorted(enrollment_totals.keys())
    data = []

    for i in range(1, len(sorted_years)):
        current_year = sorted_years[i]
        previous_year = sorted_years[i - 1]

        private_current = enrollment_totals[current_year]["Private + PSO"]
        private_previous = enrollment_totals[previous_year]["Private + PSO"]

        private_ratio = private_current / private_previous
        private_ratio = min(1.00, private_ratio)
        private_decrease = 1.00 - private_ratio

        data.append({
            "Year": f"{previous_year}-{current_year}",
            "Deficiency Ratio": private_decrease,
            "Previous Year Enrollees": private_previous,
            "Current Year Enrollees": private_current
        })

    # Convert to DataFrame for Plotly
    df_plot = pd.DataFrame(data)

    df_plot["Deficiency Ratio"] = df_plot["Deficiency Ratio"] * 100

    # Create interactive line chart
    fig = px.line(
        df_plot,
        x="Year",
        y="Deficiency Ratio",
        title="Enrollment Deficiency Ratio for Private + PSO Schools Over the Years",
        markers=True,
        labels={"Deficiency Ratio": "Deficiency Ratio"},
    )

    # Update hover template to include additional information
    fig.update_traces(
        hovertemplate=(
            "Year: %{x}<br>"
            "Deficiency Ratio: %{y:.2f}%<br>"
            "Current Year Enrollees: %{customdata[1]:,.0f}<extra></extra><br>"
            "Previous Year Enrollees: %{customdata[0]:,.0f}<br>"
        ),
        customdata=df_plot[["Previous Year Enrollees", "Current Year Enrollees"]].values,
        line=dict(color='#084683')
    )

    fig.update_layout(
        title_font=dict(size=11),
        xaxis_title="School Year",
        yaxis_title="Deficiency Ratio (%)",
        yaxis=dict(range=[0, 100]),
        template="plotly_white"
    )
    fig.update_yaxes(tickformat=".0f", ticksuffix="%")

    return fig

def indiv_private_deficiency_chart():
    import pandas as pd
    import glob
    import os
    import re
    import plotly.graph_objects as go

    # Add this as dropdown option
    # title of dropdown: By Education Level

    # Define the path and pattern for the CSV files
    folder_path = "CSV Files/"
    pattern = os.path.join(folder_path, "CLEANED_SY*_Enrollment.csv")

    # Find all matching CSV files
    csv_files = glob.glob(pattern)

    # Function to calculate total enrollees for a specific level
    def calculate_total_enrollees(df, columns):
        return df[columns].apply(pd.to_numeric, errors='coerce').sum().sum()

    # Dictionary to store totals by year for each level
    enrollment_totals = {}

    # Loop through each file and calculate totals by year
    for file in csv_files:
        match = re.search(r"SY(\d{4})", file)
        school_year = int(match.group(1)) if match else None

        if school_year:
            df = pd.read_csv(file)
            df['Sector'] = df['Sector'].astype(str).str.strip().str.title()

            # Filter for Private and PSO schools
            private_pso = df[df['Sector'].str.contains(r'\bPrivate\b|\bPso\b', na=False, regex=True)]

            # Define columns for each education level
            kinder_cols = ['K Male', 'K Female']
            elem_cols = [f'G{i} Male' for i in range(1, 7)] + [f'G{i} Female' for i in range(1, 7)]
            jhs_cols = [f'G{i} Male' for i in range(7, 11)] + [f'G{i} Female' for i in range(7, 11)]
            strands = ['STEM', 'HUMSS', 'ABM', 'GAS', 'TVL', 'SPORTS', 'ARTS', 'PBM']
            shs_cols = []
            for grade in [11, 12]:
                for strand in strands:
                    if strand in ['STEM', 'HUMSS', 'ABM', 'GAS', 'PBM']:
                        shs_cols += [f'G{grade} ACAD {strand} Male', f'G{grade} ACAD {strand} Female']
                    else:
                        shs_cols += [f'G{grade} {strand} Male', f'G{grade} {strand} Female']

            # Calculate totals for each level
            kinder_total = calculate_total_enrollees(private_pso, kinder_cols)
            elem_total = calculate_total_enrollees(private_pso, elem_cols)
            jhs_total = calculate_total_enrollees(private_pso, jhs_cols)
            shs_total = calculate_total_enrollees(private_pso, [col for col in shs_cols if col in private_pso.columns])

            # Store totals by year
            enrollment_totals[school_year] = {
                "Kindergarten": kinder_total,
                "Elementary": elem_total,
                "Junior High School": jhs_total,
                "Senior High School": shs_total
            }

    # Calculate year-over-year deficiency ratios for each level
    sorted_years = sorted(enrollment_totals.keys())
    data = []

    for i in range(1, len(sorted_years)):
        current_year = sorted_years[i]
        previous_year = sorted_years[i - 1]

        for level in ["Kindergarten", "Elementary", "Junior High School", "Senior High School"]:
            current_total = enrollment_totals[current_year][level]
            previous_total = enrollment_totals[previous_year][level]

            ratio = current_total / previous_total if previous_total > 0 else 1.0
            ratio = min(1.00, ratio)  # Cap the ratio at 1.00
            deficiency = 1.00 - ratio

            data.append({
                "Year": f"{previous_year}-{current_year}",
                "Education Level": level,
                "Deficiency Ratio": deficiency * 100,  # Convert to percentage
                "Previous Year Enrollees": previous_total,
                "Current Year Enrollees": current_total
            })

    # Convert to DataFrame
    df_plot = pd.DataFrame(data)

    # Create figure manually with one trace per education level
    fig = go.Figure()

    education_levels = df_plot["Education Level"].unique()

    for level in education_levels:
        df_level = df_plot[df_plot["Education Level"] == level]

        fig.add_trace(go.Scatter(
            x=df_level["Year"],
            y=df_level["Deficiency Ratio"],
            mode='lines+markers',
            name=level,
            meta=[level] * len(df_level),
            customdata=df_level[["Previous Year Enrollees", "Current Year Enrollees"]].values,
            hovertemplate=(
                "Year: %{x}<br>"
                "Deficiency Ratio: %{y:.2f}%<br>"
                "Previous Year Enrollees: %{customdata[0]:,.0f}<br>"
                "Current Year Enrollees: %{customdata[1]:,.0f}<extra></extra>"
            )
        ))

    fig.update_layout(
        title={"text":"Enrollment Deficiency Ratio for Private + PSO Schools by Education Level",
               "font":{"size":12}},
        xaxis_title="School Year",
        yaxis_title="Deficiency Ratio (%)",
        yaxis=dict(range=[0, 100]),
        template="plotly_white"
    )
    fig.update_yaxes(tickformat=".0f", ticksuffix="%")

    return fig

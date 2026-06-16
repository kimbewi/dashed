import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# based on figma dont use 
def k_to_10(regions, selected_region):
    # Load dataset
    df = pd.read_csv("CSV Files/CLEANED_SY2023_Enrollment.csv")

    # Melt the DataFrame
    melted_df = df.melt(id_vars=["Region"], var_name="Descriptor", value_name="Enrollees")

    # Extract Grade Level and Gender using regex (handles K to G10)
    extracted = melted_df['Descriptor'].str.extract(r'^(K|G[1-9]|G10)\s+(Male|Female)$')

    # Assign extracted columns
    melted_df['Grade Level'] = extracted[0]
    melted_df['Gender'] = extracted[1]

    # Clean and convert data
    melted_df.dropna(subset=['Grade Level', 'Gender'], inplace=True)
    melted_df['Enrollees'] = pd.to_numeric(melted_df['Enrollees'], errors='coerce').fillna(0)

    # Group data
    grouped = melted_df.groupby(['Region', 'Grade Level', 'Gender'], as_index=False)['Enrollees'].sum()

    # Grade level order
    grade_order = ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10']

    if selected_region == 'All':
            # Filter and group
            filtered = grouped.copy()
            aggregated = filtered.groupby(['Grade Level', 'Gender'], as_index=False)['Enrollees'].sum()

            # Calculate percentages and labels
            total_per_grade = aggregated.groupby('Grade Level')['Enrollees'].transform('sum')
            aggregated['Percentage'] = (aggregated['Enrollees'] / total_per_grade) * 100
            aggregated['Label'] = aggregated.apply(
                lambda row: f"{int(row['Enrollees']):,} ({row['Percentage']:.1f}%)", axis=1
            )

            # 100% stacked bar chart
            fig = px.bar(
                aggregated,
                x='Percentage',
                y='Grade Level',
                color='Gender',
                barmode='stack',
                orientation='h',
                text='Label',
                category_orders={'Grade Level': grade_order},
                color_discrete_map={'Male': '#084683', 'Female': '#DE082C'},
                title="Gender Distribution by Grade Level (All Regions)"
            )

            # Total enrollees
            total_all = int(aggregated['Enrollees'].sum())
            fig.update_layout(
                title={
                    'text': f"Gender Distribution by Grade Level (All Regions)<br><sub>Total Enrollees: {total_all:,}</sub>",
                    'x': 0.5
                },
                xaxis=dict(
                    title='Percentage',
                    ticksuffix='%',
                    range=[0, 100]
                ),
                yaxis_title='Grade Level',
                height=600,
                legend_title='Gender',
                margin=dict(l=100, r=40, t=80, b=60)
            )
            fig.update_traces(textposition='inside', insidetextanchor='middle')

    else:
            # Filter for specific region
            filtered = grouped[grouped['Region'] == selected_region]

            fig = px.bar(
                filtered,
                x='Enrollees',
                y='Grade Level',
                color='Gender',
                barmode='group',
                orientation='h',
                text='Enrollees',
                category_orders={'Grade Level': grade_order},
                color_discrete_map={'Male': '#084683', 'Female': '#DE082C'},
                title=f"Enrollees in Region {selected_region} (K to G10)"
            )

            fig.update_layout(
                xaxis_title='Number of Students',
                yaxis_title='Grade Level',
                height=600,
                legend_title='Gender',
                margin=dict(l=100, r=40, t=60, b=60)
            )
            fig.update_traces(textposition='auto')

    return fig
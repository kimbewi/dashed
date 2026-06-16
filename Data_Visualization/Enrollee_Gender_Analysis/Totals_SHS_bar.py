import pandas as pd
import plotly.express as px


def gender_shs_bar(df=None):
    # If no DataFrame was passed in, read the CSV now
    if df is None:
        df = pd.read_csv("CSV Files/CLEANED_SY2023_Enrollment.csv")

    # Melt to long format
    melted_df = df.melt(id_vars=["Region"], var_name="Descriptor", value_name="Enrollees")

    # Extract SHS Grade, Strand, Gender
    extracted = melted_df['Descriptor'].str.extract(
        r'^(G11|G12)\s*([A-Za-z\s]*)\s+(Male|Female)$'
    )
    melted_df['Grade Level'] = extracted[0]
    melted_df['Strand']      = extracted[1].str.strip()
    melted_df['Gender']      = extracted[2]

    # Drop invalid rows
    melted_df.dropna(subset=['Grade Level', 'Strand', 'Gender'], inplace=True)

    # Convert Enrollees to numeric
    melted_df['Enrollees'] = pd.to_numeric(melted_df['Enrollees'], errors='coerce').fillna(0)

    # Group data across all SHS (G11 and G12)
    grouped = melted_df.groupby(['Strand', 'Gender'], as_index=False)['Enrollees'].sum()

    # Calculate percentages for 100% stacked chart
    total_per_strand = grouped.groupby('Strand')['Enrollees'].transform('sum')
    grouped['Percentage'] = grouped['Enrollees'] / total_per_strand * 100

    # Add combined label
    grouped['Label'] = grouped.apply(
        lambda row: f"{int(row['Enrollees']):,} ({row['Percentage']:.1f}%)",
        axis=1
    )

    total_all = int(grouped['Enrollees'].sum())  # Total enrollees for all regions

    # Build the figure
    fig = px.bar(
        grouped,
        x='Percentage', y='Strand', color='Gender',
        orientation='h', barmode='stack', text='Label',
        color_discrete_map={'Male': '#084683', 'Female': '#DE082C'}, 
        title=(
            f"Gender Distribution"
            f"<br><sub>Total Enrollees for SHS: {total_all:,}</sub>"
        ),
        labels={'Percentage': 'Percentage of Students'}
    )

    fig.update_layout(
        xaxis=dict(title='Percentage', ticksuffix='%', range=[0, 100]),
        yaxis_title='Strand',
        height=385,
        legend_title='Gender',
        margin=dict(l=20, r=20, t=40, b=0)
    )
    fig.update_traces(textposition='inside', insidetextanchor='middle')

    return fig
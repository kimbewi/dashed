import plotly.graph_objects as go
import pandas as pd

def stacked_bar_chart(df):
    grouped = df.groupby(['Region', 'Modified COC'], as_index=False).size()
    coc_totals = grouped.groupby('Modified COC')['size'].sum().sort_values(ascending=False)
    coc_ranking = coc_totals.index.tolist()
    df['Modified COC'] = pd.Categorical(df['Modified COC'], categories=coc_ranking, ordered=True)
    total_schools_per_region = grouped.groupby('Region')['size'].sum().reset_index()

    custom_palette = ['#084582', '#4a669a', '#788ab3', '#a4afcc', '#d1d6e5', '#ffffff']
    custom_colors = (custom_palette * ((len(coc_ranking) // len(custom_palette)) + 1))[:len(coc_ranking)]

    fig = go.Figure()
    for i, coc in enumerate(coc_ranking):
        data = grouped[grouped['Modified COC'] == coc]
        fig.add_trace(go.Bar(
            x=data['Region'],
            y=data['size'],
            name=coc,
            marker=dict(color=custom_colors[i], line=dict(color='gray', width=1)),
            hovertemplate='<b>Modified COC:</b> %{customdata[0]}<br><b>Region:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>',
            customdata=[[coc] for _ in range(len(data))]
        ))

    for _, row in total_schools_per_region.iterrows():
        fig.add_annotation(
            x=row['Region'], y=row['size'], text=str(row['size']),
            showarrow=False, font=dict(size=12, color="black"),
            xanchor='center', yanchor='bottom'
        )

    fig.update_layout(
        #title="Number of Schools by Region and Modified COC",
        title=f"Schools by Region and Modified COC (Rows: {len(df)})",
        xaxis_title='Region',
        yaxis_title='Number of Schools',
        height=700,
        barmode='stack',
        xaxis=dict(categoryorder='total descending'),
        legend_title='Modified COC'
    )

    return fig

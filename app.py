import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import pandas as pd
from callbacks import register_callbacks
import plotly.graph_objects as go
from components.header import create_header
from components.tabs import create_tabs
from components.import_modal import import_modal
from Data_Visualization.Density_Tab_Latest.Dropout_Deficiency.Indiv_private_deficiency import indiv_private_deficiency_chart
from Data_Visualization.Density_Tab_Latest.Dropout_Deficiency.Total_deficiency_private import private_deficiency_chart
from Data_Visualization.Density_Tab_Latest.Dropout_Deficiency.Total_deficiency_public import public_deficiency_chart
from Data_Visualization.Density_Tab_Latest.Dropout_Deficiency.Indiv_public_deficiency import indiv_public_deficiency_chart

# Initialize the app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    assets_folder='assets',
    suppress_callback_exceptions=True
)

app.layout = html.Div(
    children=[
        create_header(),  # Always visible header
        import_modal(),  # Modal for file upload
        # Store holding the active dataset records
        dcc.Store(
            id="stored-data",
            data=pd.read_csv("CSV Files/CLEANED_SY2023_Enrollment.csv").to_dict('records')
        ),
        # Trigger for re-loading after processing uploads
        dcc.Store(
            id="processing-trigger",
            data=None
        ),
        # (Optional) existing menu output area
        html.Div(
            id="menu-output",
            style={"margin-top": "20px", "font-size": "18px"}
        ),

        # Main content area with tabs, wrapped in a spinner
        html.Div([
            create_tabs(),
            html.Div(id="tab-content"),
        ], style={"marginTop": "20px"}),
    ],
    style={"margin": "0", "padding": "0", "background": "#f5f5f5"}
)

# Register custom callbacks defined in callbacks.py
register_callbacks(app)

# # Density tab: update region-level heatmap
# @app.callback(
#     Output('region-level-heatmap', 'figure'),
#     Input('level-dropdown', 'value')
# )
# def update_region_heatmap_figure(selected_level):
#     from Data_Visualization.Overview_heatmap import get_region_heatmap_figure
#     return get_region_heatmap_figure(selected_level)

# Density tab: private deficiency graphs

@app.callback(
    Output('private-deficiency-graph', 'figure'),
    Input('private-deficiency-dropdown', 'value')
)
def update_private_deficiency_graph(selected_option):
    if selected_option == 'by_level':
        return indiv_private_deficiency_chart()
    return private_deficiency_chart()

# Density tab: public deficiency graphs
@app.callback(
    Output('public-deficiency-graph', 'figure'),
    Input('public-deficiency-dropdown', 'value')
)
def update_public_deficiency_chart(selected_option):
    if selected_option == 'total':
        return public_deficiency_chart()
    return indiv_public_deficiency_chart()

if __name__ == '__main__':
    app.run(port = 8051, debug=True)
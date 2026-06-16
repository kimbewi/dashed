from dash import dcc, html
import os

def create_tabs():
    # List all CSV files for selection
    options = [
        {"label": fn, "value": fn}
        for fn in os.listdir("CSV Files") if fn.endswith(".csv")
    ]

    return html.Div(
        style={"padding": "0 80px"},  # Adjusted padding to align with the main content
        children=[
            html.Div(
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "flex-end",
                },
                children=[
                    # Main tab selector with custom styles
                    dcc.Tabs(
                        id="tabs",
                        value="overview",
                        children=[
                            dcc.Tab(
                                label="Overview",
                                value="overview",
                                style={
                                    "fontFamily": "Montserrat, sans-serif",
                                    "fontSize": "16px",
                                    "color": "#084683",
                                    "backgroundColor": "transparent",
                                    "border": "none",
                                    "borderBottom": "3px solid transparent",
                                    "boxShadow": "none",
                                    "fontWeight": "normal",
                                    "padding": "6px 0 12px 0",
                                    "lineHeight": "1.5",
                                },
                                selected_style={
                                    "fontWeight": "bold",
                                    "border": "none",
                                    "borderBottom": "3px solid #084683",
                                    "boxShadow": "none",
                                    "color": "#084683",
                                    "backgroundColor": "transparent",
                                    "padding": "6px 0 12px 0",
                                    "lineHeight": "1.5",
                                    "position": "relative",
                                    "zIndex": "1",
                                },
                            ),
                            dcc.Tab(
                                label="Density",
                                value="density",
                                style={
                                    "fontFamily": "Montserrat, sans-serif",
                                    "fontSize": "16px",
                                    "color": "#084683",
                                    "backgroundColor": "transparent",
                                    "border": "none",
                                    "borderBottom": "3px solid transparent",
                                    "boxShadow": "none",
                                    "fontWeight": "normal",
                                    "padding": "6px 0 12px 0",
                                    "lineHeight": "1.5",
                                },
                                selected_style={
                                    "fontWeight": "bold",
                                    "border": "none",
                                    "borderBottom": "3px solid #084683",
                                    "boxShadow": "none",
                                    "color": "#084683",
                                    "backgroundColor": "transparent",
                                    "padding": "6px 0 12px 0",
                                    "lineHeight": "1.5",
                                    "position": "relative",
                                    "zIndex": "1",
                                },
                            ),
                        ],
                        style={"display": "flex", "gap": "24px"},
                    ),

                    # Dataset controls: dropdown for selection and upload trigger
                    html.Div(
                        style={"display": "flex", "alignItems": "center", "paddingBottom": "10px"},
                        children=[
                            dcc.Dropdown(
                                id="dataset-select",
                                options=options,
                                value="CLEANED_SY2023_Enrollment.csv",
                                clearable=False,
                                className="custom-dropdown",
                                style={
                                    "width": "250px",
                                    "marginRight": "10px",
                                    "fontFamily": "Montserrat, sans-serif",
                                    "fontSize": "14px",
                                    "color": "#084683",
                                },
                            ),
                            html.Button(
                                "+ Import Data Set",  # Matches callback ID expectations
                                id="show-upload-btn",
                                n_clicks=0,
                                style={
                                    "fontFamily": "Montserrat, sans-serif",
                                    "fontSize": "14px",
                                    "padding": "6px 16px",
                                    "backgroundColor": "transparent",
                                    "color": "#084683",
                                    "border": "2px solid #DE082C",
                                    "borderRadius": "999px",
                                    "cursor": "pointer",
                                    "marginRight": "5px",
                                },
                            ),
                            html.Div(
                                id="upload-container",
                                style={"marginLeft": "16px"},
                            ),
                        ],
                    ),
                ],
            ),

            # Underline separator
            html.Div(
                style={
                    "width": "100%",
                    "borderBottom": "1px solid #ccc",
                    "marginTop": "0",
                    "position": "relative",
                    "zIndex": "0",
                },
            ),
        ],
    )

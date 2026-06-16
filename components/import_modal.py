from dash import html, dcc

def import_modal():
    return html.Div(
        id="import-modal",
        style={"display": "none"},
        children=[
            html.Div(
                id="modal-overlay",
                style={
                    "position": "fixed",
                    "top": 0,
                    "left": 0,
                    "width": "100%",
                    "height": "100%",
                    "backgroundColor": "rgba(0,0,0,0.5)",
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "zIndex": 9999,
                },
                children=[
                    html.Div(
                        style={
                            "backgroundColor": "white",
                            "padding": "30px",
                            "borderRadius": "10px",
                            "width": "400px",
                            "position": "relative",
                            "textAlign": "center",
                        },
                        children=[
                            # X Button
                            html.Button(
                                "×",
                                id="close-modal",
                                n_clicks=0,
                                style={
                                    "position": "absolute",
                                    "top": "10px",
                                    "right": "10px",
                                    "background": "transparent",
                                    "border": "none",
                                    "fontSize": "24px",
                                    "cursor": "pointer",
                                }
                            ),
                            html.H3("Import Data Set"),
                            dcc.Upload(
                                id="upload-data",
                                children=html.Div(["Drag & Drop or ", html.A("Select a File")]),
                                style={
                                    "width": "100%",
                                    "height": "60px",
                                    "lineHeight": "60px",
                                    "borderWidth": "1px",
                                    "borderStyle": "dashed",
                                    "borderRadius": "5px",
                                    "textAlign": "center",
                                    "margin": "10px 0"
                                },
                                multiple=False
                            ),
                            html.Div(id="upload-status", style={"color": "red", "margin": "10px 0"}),
                        ]
                    )
                ]
            )
        ]
    )

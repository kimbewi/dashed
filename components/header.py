from dash import html
import datetime

def create_header():
    return html.Header(
        children=[
            # Container for the content
            html.Div(
                [
                    # Left side: Logo and Text
                    html.Div(
                        [
                            html.Img(
                                src="/assets/logo.png",
                                style={
                                    "height": "50px", #70px
                                    "margin-top": "5px",
                                    "margin-bottom": "0px",
                                }
                            ),
                            html.Div(
                                "A Department of Education Learner Information Dashboard",
                                style={"fontFamily": 'Montserrat',
                                    "font-family": "Montserrat, sans-serif",
                                    "font-size": "18px",
                                    "color": "white",
                                    "text-align": "left",
                                    "white-space": "nowrap",
                                }
                            ),
                        ],
                        style={
                            "display": "flex",
                            "flexDirection": "column",
                            "align-items": "flex-start",
                            "justify-content": "center",
                            "margin-left": "5px",
                            "margin-right": "auto",
                        }
                    ),

                    # Right side: Date and Menu Button
                    html.Div(
                        children=[
                            html.Div(
                                datetime.datetime.now().strftime("%B %d, %Y"),
                                style={ "fontFamily": 'Montserrat',
                                    "font-family": "Montserrat, sans-serif",
                                    "font-size": "18px",
                                    "color": "white",
                                    "text-align": "right",
                                    "margin-right": "20px",
                                }
                            ),
                        ],
                        style={
                            "display": "flex",
                            "align-items": "center",
                        }
                    ),
                ],
                style={
                    "display": "flex",
                    "justify-content": "space-between",
                    "align-items": "center",
                    "width": "100%",
                    "padding": "0 70px",
                },
            )
        ],
        style={
            "width": "100%",
            "background": "linear-gradient(to right, #ffffff 0.5%, #084683, #DE082C)",
            "box-shadow": "0px 4px 6px -2px gray",
            "margin": "0 0 30px 0",
            "height": "100px",
            "display": "flex",
            "justify-content": "center",
        },
    )

from dash import html

def create_footer():
    return html.Footer(
        children=[
            html.Div(
                children=[
                    html.P("© 2025 Your Company Name", style={"margin": "0"}),
                    html.Div(
                        children=[
                            html.A("Privacy Policy", href="#", style={"margin-right": "15px"}),
                            html.A("Terms of Service", href="#", style={"margin-right": "15px"}),
                            html.A("Contact Us", href="#"),
                        ],
                        style={"display": "flex"}
                    )
                ],
                style={
                    "display": "flex",
                    "justify-content": "space-between",
                    "align-items": "center",
                    "width": "100%",
                    "max-width": "1200px",
                    "margin": "0 auto",
                }
            )
        ],
        style={
            "background-color": "#b3b3b3",
            "padding": "20px 0",
            "margin-top": "30px",
            "border-radius": "20px 20px 0 0",
            "box-shadow": "0px -4px 6px -2px gray",
            "margin": "30px 30px 0 30px",
        }
    )
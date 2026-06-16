from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import os
from components.overview import create_info_card, create_two_column_layout, create_visualization_card, create_stacked_cards
from Data_Visualization.Enrollee_and_School_Analysis.modified_COCs_count import stacked_bar_chart
from Data_Visualization.density_piecharts import public_pie_chart, private_pie_chart
from Data_Visualization.density_datavis1 import get_total_schools, get_school_crowding_figure, get_subclassification_bubble_chart, add_annotation
from Data_Visualization.Density_Tab_Latest.Dropout_Deficiency.Total_deficiency_private import private_deficiency_chart
from Data_Visualization.Density_Tab_Latest.Dropout_Deficiency.Total_deficiency_public import public_deficiency_chart

total_schools = get_total_schools()

# Path to the saved pie chart images
public_pie_chart_path = 'assets/public_pie_chart.png'
private_pie_chart_path = 'assets/private_pie_chart.png'

def create_density_content():
    """Create the main dashboard content using reusable components"""
    
    # Create charts
    card1_content = html.Div([
    html.Div([
        html.Div(id="total-schools-display", style={
            'fontSize': '130px',
            'fontWeight': '400',
            'background': 'linear-gradient(90deg, rgba(8, 70, 131, 0.47) 0%, rgba(222, 8, 44, 1) 100%)',
            'WebkitBackgroundClip': 'text',
            'WebkitTextFillColor': 'transparent',
            'backgroundClip': 'text',
            'color': 'transparent',
            'fontFamily': 'Revue, Helvetica',
            'lineHeight': '1',
            'letterSpacing': '-5px',
            'marginTop': '0',
            'marginBottom': '0',
            'padding': '0',
        }),
        html.Div([
            html.H4("Schools", style={
                'marginTop': '5px',
                'color': '#084683',
                'fontFamily': 'Montserrat',
                'fontSize': '24px',
                'textAlign': 'left',
                'padding': '0',
            }),
        ])
    ], style={'padding': '0 5px', 'margin': '0'}),

    html.Div([
        dcc.Graph(id='school-crowding-chart', config={'responsive': True})
    ], style={"paddingTop": "0"}),

    html.Div([
        # Apply the annotation here
        html.P("Student Population Heatmap by Region and Strand", style={
        "fontFamily": "Google Sans, sans-serif",
        "color": "#DE082C",
        "textAlign": "left",
        "fontSize": "25px",
        "marginBottom": "0px"
    }),
        dcc.Graph(id='subclassification-bubble-chart', 
                  config={'responsive': True})
    ], style={"paddingTop": "50px", "paddingBottom": "0px"})
])

    private_content = html.Div([html.P(["Enrollee Distribution",html.Br(),"for Private and PSO Schools"], style={
        "fontFamily": "Google Sans, sans-serif",
        "color": "#DE082C",
        "textAlign": "left",
        "fontSize": "25px",
        # "marginBottom": "0px"
    }),
    html.Div(
        html.Div(
        dcc.Graph(
            id='private-pie-chart',
            #figure=private_pie_chart(),
            config={'responsive': True},
            style={"height": "240px", "width": "100%"} 
        ), style={"display": "flex", "justifyContent": "center", "alignItems": "center"}),
        style={"marginBottom": "20px"}  
    ),
    html.P("Enrollment Deficiency Analysis", style={
        "fontFamily": "Google Sans, sans-serif",
        "color": "#DE082C",
        "textAlign": "left",
        "fontSize": "20px",
        "marginBottom": "10px"
    }),

    dcc.Dropdown(
        id='private-deficiency-dropdown',
        options=[
            {'label': 'Total', 'value': 'total'},
            {'label': 'By Education Level', 'value': 'by_level'}
        ],
        value='total',
        clearable=False,
        style={
            "width": "150px",
            "height":"14px",
            "border-radius":"7px",
            "fontSize": "12px",
            "marginBottom": "23px",
            "padding": "0px 0px 0px 0px"
            }
    ),

    html.Div(
        dcc.Graph(
            id='private-deficiency-graph',
            config={'responsive': True},
            style={"height": "336px"}  
        )
    )
], style={
    "height": "750px",  
    "display": "flex",
    "flexDirection": "column"
})



    public_content = html.Div([html.P(["Enrollee Distribution",html.Br(),"for Public and SUCs/LUCs Schools"], style={
        "fontFamily": "Google Sans, sans-serif",
        "color": "#DE082C",
        "textAlign": "left",
        "fontSize": "25px",
        #"marginBottom": "0px"
    }),
    html.Div(
        html.Div(
        dcc.Graph(
            id='public-pie-chart',
            #figure=public_pie_chart(),
            config={'responsive': True},
            style={"height": "240px", "width": "100%"}  
        ),style={"display": "flex", "justifyContent": "center", "alignItems": "center"}),
        style={"marginBottom": "20px"}
    ),
    html.P("Enrollment Deficiency Analysis", style={
        "fontFamily": "Google Sans, sans-serif",
        "color": "#DE082C",
        "textAlign": "left",
        "fontSize": "20px",
        "marginBottom": "10px"
    }),

    dcc.Dropdown(
        id='public-deficiency-dropdown',
        options=[
            {'label': 'Total', 'value': 'total'},
            {'label': 'By Education Level', 'value': 'by_level'}
        ],
        value='total',
        clearable=False,
        style={
            "width": "150px",
            "height":"14px",
            "border-radius":"7px",
            "fontSize": "12px",
            "marginBottom": "23px",
            "padding": "0px 0px 0px 0px"
            }
    ),

    html.Div(
        dcc.Graph(
            id='public-deficiency-graph',
            config={'responsive': True},
            style={"height": "336px"}  
        )
    )
], style={
    "height": "750px",
    "display": "flex",
    "flexDirection": "column"
})


    card3_content = html.Div(dcc.Graph(id='stacked-bar-chart', config={'responsive': True}, style={"height": "100%"}), style={"height": "auto"})
    
    # Create components
    density_main = create_info_card("", card1_content, height=None)
    card1 = create_info_card("", private_content, height = None)
    card2 = create_info_card("", public_content, height= None)
    density_stacked_visualization = create_stacked_cards([card1, card2])


    main_section = create_two_column_layout(density_main, density_stacked_visualization)
    bottom_section = create_visualization_card(
    html.Div("Number of Schools by Region and Modified COC", style={"paddingTop": "15px", "paddingLeft":"10px"}),
    card3_content,
    height=None
    )
    
    return html.Div([
        html.Div(main_section, style={"marginBottom": "30px"}),
        bottom_section
    ], style={
        "max-width": "1400px", 
        "margin": "0 auto", 
        "padding": "10px 20px",  
        "display": "flex", 
        "flexDirection": "column",  
        "boxSizing": "border-box"
    })


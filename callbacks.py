from dash import Input, Output, State, html, dcc, callback_context
from dash.exceptions import PreventUpdate
import os, base64, subprocess, re, pandas as pd
import pandas as pd
import time
import sys
from components.overview import create_overview_content
from components.density import create_density_content
from Data_Visualization.Enrollee_Gender_Analysis.Totals_Gender_bar import gender_bar
from Data_Visualization.Enrollee_Gender_Analysis.Totals_SHS_bar import gender_shs_bar
from Data_Visualization.Overview_output import pie_chart_total_enrollees
from Data_Visualization.Timelines_Analysis.Total_Male_vs_Female_Time import enrollment_trend_by_gender
from Data_Visualization.Overview_heatmap import get_region_heatmap_figure
from Data_Visualization.phmap import phmap
from Data_Visualization.Timelines_Analysis.Total_Enrollees_Timeline import get_enrollment_trend_figure, get_latest_total_enrollees


def register_callbacks(app):
    # 1. Render page content based on selected tab
    @app.callback(
        Output("tab-content", "children"),
        Input("tabs", "value")
    )
    def render_content(tab_value):
        if tab_value == "overview":
            return create_overview_content()
        elif tab_value == "density":
            return create_density_content()
        return html.Div("No content available.")

    raw_excel_dir = "_Raw Excel Files"

    # 2. Show or hide the file upload modal
    @app.callback(
        Output("import-modal", "style"),
        Input("show-upload-btn", "n_clicks"),
        State("import-modal", "style")
    )
    def toggle_import_modal(n_clicks, current_style):
        if n_clicks and n_clicks > 0:
            # Toggle visibility based on current style
            if current_style and current_style.get("display") == "none":
                return {"display": "block"}
            return {"display": "none"}
        return {"display": "none"}

    # 3. Handle file upload: save, process, and trigger data refresh
    @app.callback(
        Output("upload-status", "children"),
        Output("processing-trigger", "data"),
        Input("upload-data", "contents"),
        State("upload-data", "filename")
    )
    def handle_upload(contents, filename):
        if not contents or not filename:
            raise PreventUpdate
        # Validate filename pattern
        pattern = re.compile(r"SY \d{4}-\d{4} School Level Data on Official Enrollment.*\.xlsx")
        if not pattern.match(filename):
            return "Invalid filename format.", None
        try:
            _, content_string = contents.split(",")
            decoded = base64.b64decode(content_string)
            filepath = os.path.join(raw_excel_dir, filename)
            with open(filepath, "wb") as f:
                f.write(decoded)
            # Run cleaning and combine scripts using the current Python interpreter
            subprocess.run([sys.executable, "Data Cleaning/data_cleaning_1.py"], check=True)
            subprocess.run([sys.executable, "Data Cleaning/combine_population.py"], check=True)
            return "File uploaded and processed successfully!", "start_processing"
        except subprocess.CalledProcessError as e:
            return f"Error in processing script: {e}", None
        except Exception as e:
            return f"Unexpected error: {e}", None

    # 4. Reload dropdown options when a new CSV appears
    @app.callback(
        Output("dataset-select", "options"),
        Input("upload-status", "children"),
        Input("processing-trigger", "data")
    )
    def update_dataset_dropdown(_, trigger_value):
        files = [f for f in os.listdir("CSV Files") if f.endswith(".csv")]
        filtered_files = [
            f for f in files if re.match(r"CLEANED_SY(\d{4})_Enrollment\.csv", f)
        ]

        # Extract years and sort descending
        sorted_files = sorted(
            filtered_files,
            key=lambda f: int(re.search(r"CLEANED_SY(\d{4})_Enrollment", f).group(1)),
            reverse=True
        )

        return [
            {
                "label": "SY" + re.search(r"CLEANED_SY(\d{4})_Enrollment\.csv", f).group(1),
                "value": f
            }
            for f in sorted_files
        ]
    
    # 6. Show which dataset is active, with row/column counts
    @app.callback(
        Output("dataset-info", "children"),
        Input("dataset-select", "value"),
        State("stored-data", "data")
    )
    def show_dataset_info(filename, stored_data):
        if not filename or not stored_data:
            return "No dataset loaded."
        df = pd.DataFrame(stored_data)
        rows, cols = df.shape
        return f"Showing “{filename}” ({rows} rows × {cols} columns)"

    # 7. Single callback to update stored-data from either a file import or dataset selection
    @app.callback(
        Output("stored-data", "data"),
        Input("processing-trigger", "data"),
        Input("dataset-select", "value")
    )
    def update_stored_data(trigger, fname):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate
        prop = ctx.triggered[0]["prop_id"]
        # Priority to processing-trigger
        if "processing-trigger.data" in prop:
            if trigger == "start_processing":
                df = pd.read_csv(os.path.join("CSV Files", "CLEANED_SY2023_Enrollment.csv"))
            else:
                raise PreventUpdate
        # Fallback to dataset-select
        elif "dataset-select.value" in prop:
            if not fname:
                raise PreventUpdate
            df = pd.read_csv(os.path.join("CSV Files", fname))
        else:
            raise PreventUpdate
        return df.to_dict("records")
    

    #  ❏ Pie chart
    @app.callback(Output("pie-chart","figure"), 
                  Input("stored-data","data"))
    
    def update_pie(_):
        return pie_chart_total_enrollees.figure

    # Gender Distribution Analysis
    @app.callback(
        Output("overview-graph", "figure"),
        Input("overview-chart-dropdown", "value"),
        Input("overview-region-dropdown",  "value"),
        Input("stored-data",               "data"),    # ← updated!
    )
    def update_overview(chart_type, region, stored_data):
        time.sleep(0.3)
        df = pd.DataFrame(stored_data or [])
        if region and region != "All Regions":
            df = df[df.Region == region]
        return (gender_shs_bar(df) if chart_type == "shs"
                else gender_bar(df))

    #  ❏ Trend chart
    @app.callback(Output("trend-chart","figure"), 
                  Input("stored-data","data"))
    def update_trend(_):
        time.sleep(0.3)
        return enrollment_trend_by_gender

    @app.callback(
        Output("region-level-heatmap", "figure"),
        Input("stored-data",    "data"),
        Input("level-dropdown", "value")
    )
    def update_region_heatmap(stored_data, level):
        time.sleep(0.3)
        df = pd.DataFrame(stored_data or [])
        return get_region_heatmap_figure(df, selected_level=level)
    
    #PH MAP
    @app.callback(
    Output("ph-map", "figure"),
    Input("stored-data", "data")
)
    def update_ph_map(stored_data):
        time.sleep(0.3)
        df = pd.DataFrame(stored_data or [])
        return phmap(df)

    #  8. Auto-refresh region dropdown options when data changes
    @app.callback(
        Output("overview-region-dropdown", "options"),
        Input("stored-data", "data")
    )
    def update_region_options(data):
        df = pd.DataFrame(data or [])
        regions = ["All Regions"] + sorted(df.Region.dropna().unique().tolist())
        return [{"label": r, "value": r} for r in regions]

    @app.callback(
        Output("combined-levels-pie","figure"),
        Input("stored-data","data")
    )
    def update_pie(data):
        time.sleep(0.3)
        df = pd.DataFrame(data or [])
        return pie_chart_total_enrollees(df)

    @app.callback(
        Output("total-enrollees-display", "children"),
        Input("dataset-select", "value")
    )
    def update_total_enrollees(selected_file):
        number = get_latest_total_enrollees(selected_file)
        return f"{number:,}"
    
    #Density - Total Schools
    @app.callback(
    Output("total-schools-display", "children"),
    Input("stored-data", "data")
    )
    def update_total_schools_display(data):
        if not data:
            raise PreventUpdate

        df = pd.DataFrame(data)
        total_schools = df.shape[0]
        return f"{total_schools:,}"
    
    #Density - Bar
    from Data_Visualization.density_datavis1 import get_school_crowding_figure

    @app.callback(
        Output("school-crowding-chart", "figure"),
        Input("stored-data", "data")
    )
    def update_school_crowding_chart(data):
        if not data:
            raise PreventUpdate
        df = pd.DataFrame(data)
        return get_school_crowding_figure(df)
    
    #Density - Heatmap
    from Data_Visualization.density_datavis1 import get_subclassification_bubble_chart

    @app.callback(
        Output("subclassification-bubble-chart", "figure"),
        Input("stored-data", "data")
    )
    def update_subclassification_chart(data):
        if not data:
            raise PreventUpdate
        df = pd.DataFrame(data)
        return get_subclassification_bubble_chart(df)
    
    #PIE - PUBLIC AND PRIVATE
    from Data_Visualization.density_piecharts import public_pie_chart, private_pie_chart

    @app.callback(
        Output('public-pie-chart', 'figure'),
        Input('stored-data', 'data')
    )
    def update_public_pie_chart(data):
        if not data:
            raise PreventUpdate
        df = pd.DataFrame(data)
        return public_pie_chart(df)
    
    @app.callback(
    Output('private-pie-chart', 'figure'),
    Input('stored-data', 'data')
    )
    def update_private_pie_chart(data):
        if not data:
            raise PreventUpdate
        df = pd.DataFrame(data)
        return private_pie_chart(df)
    
    #BAR
    from Data_Visualization.Enrollee_and_School_Analysis.modified_COCs_count import stacked_bar_chart
    from dash.exceptions import PreventUpdate

    @app.callback(
        Output('stacked-bar-chart', 'figure'),
        Input('stored-data', 'data')  # Same `stored-data` used for pie chart
    )
    def update_stacked_bar_chart(data):
        if not data:
            raise PreventUpdate
        df = pd.DataFrame(data)
        return stacked_bar_chart(df)




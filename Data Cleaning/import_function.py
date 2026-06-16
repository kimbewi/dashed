import dash
from dash import dcc, html, Input, Output, State
import os
import re
import base64
import subprocess
from dash.exceptions import PreventUpdate

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Enrollment Data Processor"

# Directories
raw_excel_dir = '_Raw Excel Files'
os.makedirs(raw_excel_dir, exist_ok=True)

# Layout
app.layout = html.Div([
    html.Div([
        html.Button("Import Dataset", id='show-upload-btn', n_clicks=0, style={'margin': '20px'}),
        html.Div(id='upload-container'),
        html.Div(id='output-message', style={'marginTop': '20px', 'textAlign': 'center'}),
        dcc.Interval(id='message-clear-interval', interval=5000, n_intervals=0, disabled=True),
        dcc.Store(id='file-processed', data=False)
    ], style={'textAlign': 'center'})
])

# Show Upload after clicking Import Dataset
@app.callback(
    Output('upload-container', 'children'),
    Output('show-upload-btn', 'style'),
    Input('show-upload-btn', 'n_clicks')
)
def display_upload(n_clicks):
    if n_clicks > 0:
        upload_box = dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag and Drop or ', html.A('Select a File')]),
            style={
                'width': '60%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '0 auto'
            },
            multiple=False
        )
        return upload_box, {'display': 'none'}
    return "", {'margin': '20px'}

# Handle upload and start processing
@app.callback(
    Output('output-message', 'children'),
    Output('file-processed', 'data'),
    Output('upload-container', 'style'),
    Output('message-clear-interval', 'disabled'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def handle_upload(contents, filename):
    if contents and filename:
        # Show processing message first
        processing_msg = "⏳ Processing file..."

        # Validate filename
        pattern = re.compile(r'SY \d{4}-\d{4} School Level Data on Official Enrollment.*\.xlsx')
        if not pattern.match(filename):
            return " Invalid file format. Please upload a properly named file.", False, {'display': 'none'}, True

        try:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            file_path = os.path.join(raw_excel_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(decoded)
        except Exception as e:
            return f" Error saving file: {e}", False, {'display': 'none'}, True

        # Show processing message before executing
        return processing_msg, "start_processing", dash.no_update, True

    raise PreventUpdate

# Actually run the cleaning scripts after message is set
@app.callback(
    Output('output-message', 'children', allow_duplicate=True),
    Output('message-clear-interval', 'disabled', allow_duplicate=True),
    Output('file-processed', 'data', allow_duplicate=True),
    Input('file-processed', 'data'),
    prevent_initial_call='initial_duplicate'
)
def run_processing(data_status):
    if data_status != "start_processing":
        raise PreventUpdate

    try:
        subprocess.run(['python3', 'Data Cleaning/data_cleaning_1.py'], check=True)
        subprocess.run(['python3', 'Data Cleaning/combine_population.py'], check=True)
        return " File processed successfully!", False, True
    except subprocess.CalledProcessError as e:
        return f" Error during processing: {e}", True, False

# After 5s, hide message and bring back Import button
@app.callback(
    Output('output-message', 'children', allow_duplicate=True),
    Output('upload-container', 'children', allow_duplicate=True),
    Output('show-upload-btn', 'style', allow_duplicate=True),
    Output('message-clear-interval', 'disabled', allow_duplicate=True),
    Input('message-clear-interval', 'n_intervals'),
    prevent_initial_call=True
)
def reset_interface(n_intervals):
    return "", "", {'margin': '20px'}, True

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

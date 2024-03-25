from dash import dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import base64
from PIL import Image

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

def encode_image(image_path):
    with open(image_path, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()
    return f"data:image/jpeg;base64,{encoded_image}"


df = pd.read_csv('data/observables/combinedData/averagedObservables.csv')

snapshotPath = "data/outputImages/snapshots/delay_0/Noise=0.400000_Delay=0.png"
app.layout = html.Div(
    children=[
        html.Div(
                children=[
                    html.H4("Delayed Vicsek Model"),
                ],
            ),
            html.Div(
                children=[
                html.P('Selected Delay Amount'),
                 dcc.Checklist(                 
                     options=df['Delay'].unique(),
                     value=[0,1,3,5],
                     id='selectedDelays',
                     inline=True
                    ),
                     
                ], style={'width': '49%', 'display': 'inline-block'}
            ),
             html.Div(
                 children=[
                     html.P('Select Observable'),
                     dcc.Dropdown(
                     options = list(df.columns)[2:7],
                     value= df.columns[2],
                     id = 'selectedAverageObservable')
                 ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}
          ),
        html.Div(
            children=[
                html.Div(
                 dcc.Graph(id="orderParameter")
                ),
            ], style={"width": "50%", "float": "left"},  # Set graph width and position
        ),
        html.Div(
            children=[
                html.Img(id='snapshot', src=encode_image('data/outputImages/snapshots/delay_0/Noise=0.472000_Delay=0.png'),  style={"width": "50%"}),
             ], style={"width": "50%", "float": "right"},  # Set image width and position       
        ),
        html.Div(
            children=[
                dcc.Graph(id="timeSeries")    
            ], style={"width": "100%", "display": "flex", "flex-direction": "column"}
        ),
            html.Div([
            dcc.Markdown("""
            """),
            html.H1(id='click-data'),
        ], className='three columns'),
]
)




@callback(
    Output("orderParameter", "figure"),
    Input("selectedDelays", "value"),
    Input("selectedAverageObservable", "value"),
    )
def update_graph(selectedDelay, selectedAverageObservable):

    filtered_df = df[df['Delay'].isin(selectedDelay)]
    fig = px.scatter(filtered_df, x=filtered_df['Noise'],
            y=filtered_df[selectedAverageObservable])
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    
    return fig

@callback(
    Output("click-data", "children"),
    Input('orderParameter', 'clickData'))
def updateSnapshot(clickData):
    
    if clickData is None:
        snapshotPath='piss'
    else:
        pointNumber=clickData['points'][0]['pointNumber']
        snapshotPath = str(df.loc[pointNumber,'timeseriesPath'])  # Replace with your logic

    return snapshotPath


@callback(
    Output('snapshot', 'src'),
    Input('orderParameter', 'clickData'))
def display_click_data(clickData):

    if clickData:
        pointNumber=clickData['points'][0]['pointNumber']

        snapshotPath = df.loc[pointNumber,'snapshotPath'] # Replace with your logic
    else:
        snapshotPath = "data/outputImages/snapshots/delay_0/Noise=0.400000_Delay=0.png"  # Set to empty string if no value

    return encode_image(snapshotPath)

@callback(
    Output('timeSeries', 'figure'),
    Input('orderParameter', 'clickData')
)
def update_timeseries_fig(clickData):
    fig=px.line()
    if clickData:
        pointNumber=clickData['points'][0]['pointNumber']
        timeseriesPath= df.loc[pointNumber,'timeseriesPath']
        timeseries= pd.read_csv(str(timeseriesPath), skiprows=3)
        fig=px.line(timeseries, x='time', y='Order')
    return fig

if __name__ == '__main__':
    app.run(debug=True,port=8080)
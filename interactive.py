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


df = pd.read_csv('data/combinedData/averagedObservables2.csv')
df['Delay']= df['Delay'].astype(str)

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
                    
                dcc.Graph(
                    id="orderParameter",
                    figure=px.scatter(df,
                                      x='Noise', 
                                      y='Average Polar Orderparameter', 
                                      color='Delay' ,hover_data={'Custom': True})

                ),
                )
            ], style={"width": "100%", "float": "left"},  # Set graph width and position
        ),
        html.Div(
            children=[
                html.Img(id='snapshot', src=encode_image('data/outputImages/snapshots/delay_0/delayTime=0_noiseStrength=0.4000.png'),  style={"width": "50%"}),
             ], style={"width": "50%", "float": "right"},  # Set image width and position       
        ),
        html.Div(
            children=[
                html.Img(id="timeSeries", src=encode_image('data/outputImages/timeSeries/delay_0/delayTime=0_noiseStrength=0.4000.png'))    
            ], style={"width": "50%", "float": "left"}
        )
]
)




@callback(
    Output("orderParameter", "figure"),
    Input("selectedDelays", "value"),
    Input("selectedAverageObservable", "value"),
    )
def update_graph(selectedDelay, selectedAverageObservable):
    if selectedDelay is None:
        selectedDelay = 0
        figure = px.scatter(df, x=df['Noise'],
                y=df[selectedAverageObservable],color=df['Delay'], hover_data={'Custom': True})
    
    else:
        filtered_df = df[df['Delay'].isin(selectedDelay)]
        figure = px.scatter(filtered_df, x=filtered_df['Noise'],
                y=filtered_df[selectedAverageObservable], delay=df['Delay'], hover_data={'Custom': True})
    
    return figure


@callback(
    Output('snapshot', 'src'),
    Input('orderParameter', 'clickData'),
    )

    
def display_click_data(clickData):
    global df
    if clickData:
        pointNumber=clickData['points'][0]['pointIndex']
        original_index = df.loc[pointNumber, 'OriginalIndex']
        snapshotPath = df.loc[original_index,'snapshotPath'] # Replace with your logic
    else:
        snapshotPath = "data/outputImages/snapshots/delay_0/delayTime=0_noiseStrength=0.4000.png"  # Set to empty string if no value

    return encode_image(snapshotPath)

@callback(
    Output('timeSeries', 'src'),
    Input('orderParameter', 'clickData')
)
def update_timeseries_fig(clickData):
    global df
    if clickData:
        pointNumber=clickData['points'][0]['pointIndex']
        original_index = df.loc[pointNumber, 'OriginalIndex']

        snapshotPath = df.loc[original_index,'timeseriesPath'] 
    else:
        snapshotPath = "data/outputImages/timeSeries/delay_0/delayTime=0_noiseStrength=0.4000.png"  # Set to empty string if no value

    return encode_image(snapshotPath)

if __name__ == '__main__':
    app.run(debug=True,port=8080)
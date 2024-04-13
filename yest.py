import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Sample DataFrame
df = pd.DataFrame({
    'X': [1, 2, 3, 4, 5],
    'Y': [10, 20, 30, 40, 50],
    'Label': ['A', 'B', 'C', 'D', 'E'],
    'Custom': [f'CustomData-{i}' for i in range(5)]
})

app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    dcc.Graph(
        id='scatter-plot',
        figure=px.scatter(
            df, x='X', y='Y', hover_data={'Custom': True}, 
            title='Scatter Plot'
        )
    ),
    html.Div(id='selected-point')
])

# Define callback to update the selected-point div based on clickData
@app.callback(
    Output('selected-point', 'children'),
    [Input('scatter-plot', 'clickData')]
)
def display_selected_point(clickData):
    if clickData is not None and 'points' in clickData:
        # Extract custom data from the clicked point
        point_index = clickData['points'][0]['pointIndex']
        selected_value = df.loc[point_index, 'Custom']
        return f'Selected point custom data: {selected_value}'
    else:
        return 'Click on a point to display its custom data'

if __name__ == '__main__':
    app.run_server(debug=True)

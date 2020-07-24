import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd
import json
from datetime import datetime as dt, timedelta

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Wybory prezydenckie 2020'
server = app.server


def prepare_dataframe(file_name):
    df = pd.read_csv(file_name, sep=';')
    df["wygrany"] = (df['Andrzej Sebastian DUDA']/df['Rafał Kazimierz TRZASKOWSKI']).astype('float')
    df["wygrany_bool"] = (df['Andrzej Sebastian DUDA']>df['Rafał Kazimierz TRZASKOWSKI']).astype('int')
    df["TERYT"] = df["Kod TERYT"].apply(lambda s: str(s)[:-2])
    df["TERYT"] = df["TERYT"].astype('int')
    return df

def prepare_chart(area, type):
    if area=="P":
        df = df_powiaty
        locations = df['TERYT']
        featureidkey = 'properties.JPT_KOD_JE'
        file_name = "powiaty.json"
        customdata = pd.np.stack((df['Powiat'], df['Andrzej Sebastian DUDA'], df['Rafał Kazimierz TRZASKOWSKI']),
                                 axis=-1)
        hovertemplate = 'Powiat: %{customdata[0]}<br>' + \
                        'ANDRZEJ DUDA: %{customdata[1]}<br>' + \
                        'RAFAŁ TRZASKOWSKI: %{customdata[2]}<extra></extra>'
    else:
        df = df_woj
        locations = df['Województwo']
        featureidkey = 'properties.JPT_NAZWA_'
        file_name = "wojewodztwa.json"
        customdata = pd.np.stack((df['Województwo'], df['Andrzej Sebastian DUDA'], df['Rafał Kazimierz TRZASKOWSKI'],
                                  df['Andrzej Sebastian DUDA']/df['Rafał Kazimierz TRZASKOWSKI']),
                                 axis=-1)
        hovertemplate = 'Woj.: %{customdata[0]}<br>' + \
                        'ANDRZEJ DUDA: %{customdata[1]}<br>' + \
                        'RAFAŁ TRZASKOWSKI: %{customdata[2]}<br><extra></extra>'

    col_z = df["wygrany_bool"]
    showscale = False
    if type=="1":
        col_z = df["wygrany"]
        showscale = True
    if type=="2":
        col_z = df["Liczba głosów nieważnych"]
        showscale = True
        customdata = pd.np.stack((df["Liczba głosów nieważnych"],),
                                 axis=-1)
        hovertemplate = 'Liczba głosów nieważnych: %{customdata[0]}<extra></extra>'

    with open(file_name , "rt") as fd:
        counties = json.load(fd)
    for x in range(0, len(counties['features'])):
        counties['features'][x]["properties"]['JPT_KOD_JE'] = int(counties['features'][x]["properties"]['JPT_KOD_JE'])

    fig = go.Figure(go.Choroplethmapbox(geojson=counties,
                                        locations=locations,
                                        z=col_z,
                                        showscale=showscale,
                                        featureidkey=featureidkey,
                                        colorscale ="blues",# [[0, 'rgb(0,255,0)'], [1, 'rgb(127,127,255)']],
                                        customdata=customdata,
                                        hovertemplate=hovertemplate,
                                        marker_line_width=1))

    fig.update_layout(autosize=False,
                      width=900,  height=700,
                      margin=dict( l=10, r=10, b=10, t=40, pad=4),
                      mapbox=dict(style='carto-positron', zoom=5.5,
                                  center = {"lat": 52.1022602 , "lon":19.3721183 }));
    return fig


# DataFrame z wynikami
df_powiaty = prepare_dataframe("wyniki-powiaty.csv")
df_woj = prepare_dataframe("wyniki-wojewodztwa.csv")

app.layout = html.Div([

    html.H3(children='Wyniki wyborów prezydenckich - 2 tura'),

    html.Table([
        html.Tr([
            html.Td(
                dcc.Dropdown(
                    id='dropdown_area',
                    options=[
                        {'label': 'województwa', 'value': 'W'},
                        {'label': 'powiaty', 'value': 'P'},
                    ],
                    value='P',
                    style={"width":"100%"}
                ), style={"width":"50%"}
            ),

            html.Td(
                dcc.Dropdown(
                    id='dropdown_type',
                    options=[
                        {'label': 'wygrana kandydatów', 'value': '0'},
                        {'label': 'stosunek głosów oddanych na kandydatów (A.Duda vs R.Trzaskowski)', 'value': '1'},
                        {'label': 'liczba głosów nieważnych', 'value': '2'},
                    ],
                    value='0',
                    style={"width":"100%"}
                ), style={"width":"50%"}
            ),

        ])
    ], style={"width":"80%"}),

    #dcc.Graph(id='graph-1', style={"width":"100%"} ),
    html.Div(id='output'),

], style={"margin":"20px", })

@app.callback(
    #Output('graph-1', 'figure'),
    Output(component_id='output', component_property='children'),
    [Input('dropdown_area', 'value'),
     Input('dropdown_type', 'value')])
def update_graph(dropdown_area,dropdown_type):
    graphs = []
    fig = prepare_chart(dropdown_area, dropdown_type)
    g = dcc.Graph(id='graph-1', style={"width": "100%"}, figure=fig)
    graphs.append(html.Div(g))
    return graphs



if __name__ == '__main__':
    app.run_server(debug=True)
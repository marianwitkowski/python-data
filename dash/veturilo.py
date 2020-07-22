import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import datetime as dt, timedelta

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('veturilo.csv').sort_values('ts')

df_stations = pd.read_csv('stations.csv')
stations_list = [{"label":s[1], "value":s[0]} for s in list(df_stations.values)]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Veturilo - dane historyczne'

app.layout = html.Div([

    html.H3(children='Dostępność rowerów Veturilo'),

    dcc.Dropdown(
        id='dropdown_station',
        placeholder='Wybierz stację...',
        options= stations_list, style={"margin":"5px", "width":"80%"},
        clearable=True,
    ),

    html.Br(),
    dcc.DatePickerRange(
        id="daterange_station",
        start_date=dt.now()-timedelta(7),
        end_date=dt.now(),
        display_format='YYYY-MM-DD',
        style={"margin":"10px"}
    ),

    html.Button(id='button-1', children='Pokaż dostępność', n_clicks=0, style={"margin":"10px"}),
    dcc.Graph(id='graph-1'),

], style={"margin":"20px", })

@app.callback(
    Output('graph-1', 'figure'),
    [Input('button-1', 'n_clicks')],
    [State('dropdown_station', 'value'),
     State('daterange_station', 'start_date'), State('daterange_station', 'end_date')])
def update_graph(n_clicks,dropdown_station,ts_start, ts_stop):
    print(dropdown_station, ts_start, ts_stop, sep='|')
    if not dropdown_station is None:
        ts_start = str(ts_start[:10])
        ts_stop = str(ts_stop[:10])
        df_tmp = df[(df.ts>=ts_start)&(df.ts<=ts_stop)]
        df_tmp = df_tmp[df_tmp.uid == dropdown_station]
        df_tmp["MA"]= df_tmp.qnty.rolling(24).mean()
        station_name = df_stations[df_stations.uid==dropdown_station].iloc[0]["name"]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_tmp["ts"], y=df_tmp["qnty"],
                                 mode='lines', line={"color":"green"},
                                 name='dostępna liczba'))

        fig.add_trace(go.Scatter(x=df_tmp["ts"], y=df_tmp["MA"],
                                 mode='lines', line={"color":"magenta"},
                                 name='średnia krocząca 2h'))

        fig.update_layout(height=600, title_text=f'Dane historycznee - stacja {station_name}')
        return fig
    else:
        return {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "Wybierz stację i przedział czasowy" if dropdown_station is None else "Brak danych",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ]
            }
        }

if __name__ == '__main__':
    app.run_server(debug=False)
from dash import Dash
import pandas as pd
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from preprocessing import preprocess
from visualisation import gender_plots, temperature_and_season, workday_and_dayoff, trips_dynamics, stations, routes
from const import BLACK, WHITE

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

@app.callback(Output('hist1', 'figure'),
              [Input('histogram-selector1', 'value')])
def update_histogram1(selected_value):
    if selected_value == 'dayoff hist':
        return fig_dayoff
    elif selected_value == 'workday hist':
        return fig_workday


@app.callback(Output('hist2', 'figure'),
              [Input('histogram-selector2', 'value')])
def update_histogram2(selected_value):
    print(f"update_histogram2: {selected_value}")
    if selected_value == 'duration':
        print('duration')
        return fig_temperature_mean_duration
    else:
        print('frequency')
        return fig_temperature_count_trips


@app.callback(Output('hist3', 'figure'),
              [Input('histogram-selector3', 'value')])
def update_histogram3(selected_value):
    print(f"update_histogram3: {selected_value}")
    if selected_value == 'duration':
        print('duration')
        return fig_workday_and_dayoff_mean_duration
    else:
        print('frequency')
        return fig_workday_and_dayoff_count_trips


@app.callback(Output('hist4', 'figure'),
              [Input('histogram-selector4', 'value')])
def update_histogram4(selected_value):
    print(f"update_histogram4: {selected_value}")
    if selected_value == 'top5':
        return fig_stations_top
    else:
        return fig_stations_bottom



df = pd.read_csv('data.csv')
df = preprocess(df)

fig_proportion, fig_dayoff, fig_workday = gender_plots(df)

fig_temperature_mean_duration = temperature_and_season(df, 'mean')
fig_temperature_count_trips = temperature_and_season(df, 'count')

fig_workday_and_dayoff_mean_duration = workday_and_dayoff(df, 'mean')
fig_workday_and_dayoff_count_trips = workday_and_dayoff(df, 'count')

fig_trips_dynamics = trips_dynamics(df)

fig_stations_top = stations(df, 'top')
fig_stations_bottom = stations(df, 'bottom')

fig_routes = routes(df)

app.layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                dbc.Row([
                    html.H1('Divvy Bikes\nDashboard', style={'color': WHITE}),
                    dcc.Graph(id='proportion', figure=fig_proportion),
                    dcc.Dropdown(
                                id='histogram-selector1',
                                options=[
                                    {'label': html.Span('Durée du voyage le weekend/jour férié', style={'color': WHITE, 'background': BLACK}), 'value': 'dayoff hist'},
                                    {'label': html.Span('Durée du voyage le jour ouvré', style={'color': WHITE, 'background': BLACK}), 'value': 'workday hist'}
                                ],
                                value='workday hist',
                                style={'width': '70%', 'background': BLACK, "color": WHITE, 'align': 'center'}
                        ),
                    dcc.Graph(
                            id='hist1',
                    ),
                ])
            ),
            dbc.Col(
                dbc.Row([
                    html.Div([
                        dcc.Dropdown(
                                id='histogram-selector2',
                                options=[
                                    {'label': html.Span('Durée des voyages', style={'color': WHITE, 'background': BLACK}), 'value': 'duration'},
                                    {'label': html.Span('Nombre des voyages', style={'color': WHITE, 'background': BLACK}), 'value': 'frequency '}
                                ],
                                value='duration',
                                style={'width': '60%', 'background': BLACK, "color": WHITE}
                        ),
                        dcc.Graph(id='hist2', figure=fig_temperature_mean_duration),
                    ])])
            ),
            dbc.Col(
                dbc.Row([
                    html.Div([
                        dcc.Dropdown(
                                id='histogram-selector3',
                                options=[
                                    {'label': html.Span('Durée des voyages', style={'color': WHITE, 'background': BLACK}), 'value': 'duration'},
                                    {'label': html.Span('Nombre des voyages', style={'color': WHITE, 'background': BLACK}), 'value': 'frequency '}
                                ],
                                value='duration',
                                style={'width': '60%', 'background': BLACK, "color": WHITE}
                        ),
                        dcc.Graph(id='hist3', figure=fig_temperature_mean_duration),
                    ])])
            )
            ], align="center"),
    dbc.Row([dcc.Graph(id='rips_dynamics', figure=fig_trips_dynamics)]),
    dbc.Row([
        dbc.Col(),
        dbc.Col([
            dcc.Dropdown(
                    id='histogram-selector4',
                    options=[
                        {'label': html.Span("Top 5", style={'color': WHITE, 'background': BLACK}), 'value': 'top5'},
                        {'label': html.Span("Bottom 5", style={'color': WHITE, 'background': BLACK}), 'value': 'bottom5 '}
                    ],
                    value='top5',
                    style={'width': '50%', 'background': BLACK, "color": WHITE, 'text-align':'center'}

            ),
        dbc.Col()
    ]),
    dbc.Row([dcc.Graph(id='hist4', figure=fig_stations_top)])]),
    dbc.Row([dcc.Graph(id='hist5', figure=fig_routes)])
], style={'background-color': BLACK}
)

if __name__ == '__main__':
    app.run_server(debug=True)
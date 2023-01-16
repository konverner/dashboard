import numpy as np
import pandas as pd
import matplotlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

from const import TEMPLATE, BLACK, GREEN, YELLOW, BLUE, RED


pio.templates["template_custom"] = pio.templates["plotly_dark"]
pio.templates["template_custom"]['layout']['paper_bgcolor'] = BLACK
pio.templates["template_custom"]['layout']['plot_bgcolor'] = BLACK


def colorGradient(c1: str, c2: str, n: int):
    c1 = np.array(matplotlib.colors.to_rgb(c1))
    c2 = np.array(matplotlib.colors.to_rgb(c2))
    return [matplotlib.colors.to_hex((1-(i/n))*c1 + (i/n)*c2) for i in range(n)]


def gender_plots(df):
    male_dayoff_duration = df[df['gender'] == 'Male'].loc[(df['Holiday'] == 1) | (df['Weekend'] == 1)]['tripduration']
    male_workday_duration = df[df['gender'] == 'Male'].loc[(df['Holiday'] == 0) & (df['Weekend'] == 0)]['tripduration']

    female_dayoff_duration = df[df['gender'] == 'Female'].loc[(df['Holiday'] == 1) | (df['Weekend'] == 1)]['tripduration']
    female_workday_duration = df[df['gender'] == 'Female'].loc[(df['Holiday'] == 0) & (df['Weekend'] == 0)]['tripduration']

    proportion = go.Pie(values=df['gender'].value_counts().values, labels=['Homme', 'Femme'],
               marker=dict(colors=[BLUE, RED]))
    layout_proportion = go.Layout(title="La proportion d'utilisateurs", width=400, height=400, template=TEMPLATE)
    fig_proportion = go.Figure(data=[proportion], layout=layout_proportion)

    trace_dayoff_male = go.Histogram(x=male_dayoff_duration.values, marker=dict(color=BLUE), showlegend=False)
    trace_dayoff_female = go.Histogram(x=female_dayoff_duration.values, marker=dict(color=RED), showlegend=False)
    layout_dayoff = go.Layout(title='', barmode='overlay', width=700, height=450, template=TEMPLATE)
    fig_dayoff = go.Figure(data=[trace_dayoff_male, trace_dayoff_female], layout=layout_dayoff)
    fig_dayoff.update_yaxes(title_text="# voyages")
    fig_dayoff.update_xaxes(title_text="min")

    trace_workday_male = go.Histogram(x=male_workday_duration.values, marker=dict(color=BLUE), showlegend=False)
    trace_workday_female = go.Histogram(x=female_workday_duration.values, marker=dict(color=RED), showlegend=False)
    layout_workday = go.Layout(title='', barmode='overlay', width=700, height=450, template=TEMPLATE)
    fig_workday = go.Figure(data=[trace_workday_male, trace_workday_female], layout=layout_workday)
    fig_workday.update_yaxes(title_text="# voyages")
    fig_workday.update_xaxes(title_text="min")

    return fig_proportion, fig_dayoff, fig_workday


def temperature_and_season(df, agg_func='mean'):

    fig = make_subplots(rows=3, cols=1)
    fig.update_xaxes(title_text="mois", row=1, col=1)
    fig.update_xaxes(title_text="temperature en °C", row=2, col=1)
    fig.update_xaxes(title_text="evenement météo", row=3, col=1)

    if agg_func == 'mean':
        fig.update_yaxes(title_text="min", row=1, col=1)
        fig.update_yaxes(title_text="min", row=2, col=1)
        fig.update_yaxes(title_text="min", row=3, col=1)
        df_month_duration = df.groupby('month')['tripduration'].mean()
        df_temp = df.groupby('temperature')['tripduration'].mean()
        df_events = df.groupby('events')['tripduration'].mean().drop('unknown')

    if agg_func == 'count':
        fig.update_yaxes(title_text="# voyages", row=1, col=1)
        fig.update_yaxes(title_text="# voyages", row=2, col=1)
        fig.update_yaxes(title_text="# voyages", row=3, col=1)
        df_month_duration = df.groupby('month')['trip_id'].count()
        df_temp = df.groupby('temperature')['trip_id'].count()
        df_events = df.groupby('events')['trip_id'].count()

    fig.add_trace(go.Bar(x=df_month_duration.keys(), y=df_month_duration.values, marker=dict(
        color=[BLUE, BLUE, GREEN, GREEN, GREEN, RED, RED, RED, YELLOW, YELLOW, YELLOW, BLUE])), row=1, col=1)
    fig.add_trace(go.Bar(x=df_temp.keys(), y=df_temp.values, width=0.6,
                         marker=dict(color=colorGradient(BLUE, RED, len(df_temp)))), row=2, col=1)
    fig.add_trace(go.Bar(x=df_events.keys(), y=df_events.values, marker=dict(color=BLUE)), row=3,
                  col=1)
    fig.update_layout(
        height=900,
        width=600,
        bargap=0.2,
        showlegend=False,
        template=TEMPLATE,
    )
    return fig


def workday_and_dayoff(df, agg_func='mean'):

    fig = make_subplots(rows=3, cols=1, specs=[[{"type": "pie"}], [{"type": "bar"}], [{"type": "bar"}]],
                        subplot_titles=(
                        "Proportion de voyages dans différents jours", "Répartition des voyages sur la jour ouvré",
                        "Répartition des voyages sur la jour non ouvré"))

    if agg_func == 'count':
        fig.update_yaxes(title_text="# voyages", row=2, col=1)
        fig.update_yaxes(title_text="# voyages", row=3, col=1)
        dayoff = df[(df['Holiday'] == 1) | (df['Weekend'] == 1)].groupby('hour')['trip_id'].count()
        workday = df[(df['Holiday'] == 0) & (df['Weekend'] == 0)].groupby('hour')['trip_id'].count()

    if agg_func == 'mean':
        fig.update_yaxes(title_text="min", row=2, col=1)
        fig.update_yaxes(title_text="min", row=3, col=1)
        dayoff = df[(df['Holiday'] == 1) | (df['Weekend'] == 1)].groupby('hour')['tripduration'].mean()
        workday = df[(df['Holiday'] == 0) & (df['Weekend'] == 0)].groupby('hour')['tripduration'].mean()

    dayoff_count = df[(df['Holiday'] == 1) | (df['Weekend'] == 1)]['trip_id'].count()
    workday_count = df[(df['Holiday'] == 0) & (df['Weekend'] == 0)]['trip_id'].count()

    fig.add_trace(go.Pie(labels=['Jour ouvré', 'Weekend/Jour férié'], values=[workday_count, dayoff_count],
                         marker=dict(colors=[BLUE, RED])), row=1, col=1)

    fig.add_trace(
        go.Bar(x=dayoff.keys(), y=dayoff.values, width=0.6, marker=dict(color=BLUE)), row=2, col=1)
    fig.add_trace(
        go.Bar(x=workday.keys(), y=workday.values, width=0.6, marker=dict(color=RED)), row=3, col=1)

    fig.update_layout(
        height=900,
        width=600,
        bargap=0.2,
        showlegend=False,
        template=TEMPLATE,
    )
    return fig


def trips_dynamics(df):

    months_trips_counts = df.groupby(['year', 'month'])['trip_id'].count()

    x = range(len(months_trips_counts.values))
    z = np.polyfit(x, months_trips_counts.values, 1)

    fig = make_subplots(rows=1, cols=1)

    fig.add_trace(go.Scatter(x=list(range(len(months_trips_counts.values))), y=months_trips_counts.values, mode='lines',
                             line=dict(color=BLUE),showlegend=False))
    fig.add_trace(go.Scatter(x=list(range(len(months_trips_counts.values))),
                             y=np.poly1d(np.polyfit(x, months_trips_counts.values, 1))(x), mode='lines',
                             line=dict(color=BLUE), showlegend=False))

    fig.update_layout(title='La Croissance de la Location de Vélos', xaxis_title='an, mois', template=TEMPLATE)
    fig.update_xaxes(tickvals=list(range(len(months_trips_counts)))[::5], ticktext=list(months_trips_counts.index)[::5])
    return fig


def stations(df, mode='top'):
    pivot_table1 = pd.pivot_table(df, index=['from_station_name'], columns=['year'], values=['trip_id'],
                                  aggfunc='count')
    pivot_table2 = pd.pivot_table(df, index=['to_station_name'], columns=['year'], values=['trip_id'], aggfunc='count')

    old_stations1 = []  # since 2015
    old_stations2 = []

    for station_name in pivot_table1.index:
        if not pd.isna(sum(pivot_table1.loc[station_name])):
            old_stations1.append(station_name)

    for station_name in pivot_table2.index:
        if not pd.isna(sum(pivot_table1.loc[station_name])):
            old_stations2.append(station_name)

    old_stations = set(old_stations1 + old_stations2)
    df_old_stations = df[(df['from_station_name'].isin(old_stations)) & (df['to_station_name'].isin(old_stations))]

    if mode == 'top':
        stations_from = df_old_stations['from_station_name'].value_counts()[:5]
        stations_to = df_old_stations['to_station_name'].value_counts()[:5]

    else:
        stations_from = df_old_stations['from_station_name'].value_counts()[-5:]
        stations_to = df_old_stations['to_station_name'].value_counts()[-5:]

    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "bar"}]],
                        subplot_titles=(
                            "Stationnements de départ", "Stationnements à l'arrivée"))


    fig.add_trace(go.Bar(
        y=list(stations_from.keys()),
        x=list(stations_to.values),
        orientation='h',
        marker=dict(color=BLUE),
        showlegend=False
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        y=list(stations_from.keys()),
        x=list(stations_to.values),
        orientation='h',
        marker=dict(color=RED),
        showlegend=False
    ), row=1, col=2)

    fig.update_layout(
        xaxis_title='frequence de voyages',
        template=TEMPLATE,
    )

    return fig


def routes(df):
    pivot_table1 = pd.pivot_table(df, index=['from_station_name'], columns=['year'], values=['trip_id'],
                                  aggfunc='count')
    pivot_table2 = pd.pivot_table(df, index=['to_station_name'], columns=['year'], values=['trip_id'], aggfunc='count')

    old_stations1 = []  # since 2015
    old_stations2 = []

    for station_name in pivot_table1.index:
        if not pd.isna(sum(pivot_table1.loc[station_name])):
            old_stations1.append(station_name)

    for station_name in pivot_table2.index:
        if not pd.isna(sum(pivot_table1.loc[station_name])):
            old_stations2.append(station_name)

    old_stations = set(old_stations1 + old_stations2)
    df_old_stations = df[(df['from_station_name'].isin(old_stations)) & (df['to_station_name'].isin(old_stations))]
    top5_pairs = df_old_stations[['from_station_name', 'to_station_name']].value_counts().reset_index(name='count')[:5]

    fig = go.Figure(data=[
        go.Bar(y=top5_pairs['from_station_name'] + ' --> ' + top5_pairs['to_station_name'], x=top5_pairs['count'],
               orientation='h', marker=dict(color=BLUE))])
    fig.update_layout(title_text='Trajets plus populaires', xaxis_title='Voyages', template=TEMPLATE)
    return fig

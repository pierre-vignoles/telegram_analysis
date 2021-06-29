from datetime import datetime
from typing import List, Dict
import plotly.graph_objs as go
import pandas as pd

from Viz import color_graph


def function_number_of(df: pd.DataFrame, media: str, list_names: list, month_or_day: str,
                       dict_media: Dict[str, str]) -> go.Figure:
    df_copy: pd.DataFrame = df.copy()
    df_copy['date'] = df_copy['datetime'].apply(lambda x: x.date())
    df_copy['month'] = df_copy['datetime'].apply(lambda x: x.month)
    df_copy['year'] = df_copy['datetime'].apply(lambda x: x.year)
    df_copy['text'] = df['text'].apply(lambda x: str(x))
    dict_df_names: Dict[str] = {}
    dict_tmp: Dict[str] = {}

    if media == 'text':
        for name in list_names:
            if month_or_day == 'day':
                dict_df_names[name] = \
                    df_copy.loc[(df_copy['from'] == name) & (df_copy['text'] != 'NaNValue'), :].groupby(['date'])[
                        media].count().to_frame().reset_index().sort_values(by='date')
            elif month_or_day == 'month':
                dict_df_names[name]: Dict[str, int] = {}
                dict_tmp[name]: Dict[pd.Series] = \
                    df_copy.loc[(df_copy['from'] == name) & (df_copy['text'] != 'NaNValue'), :].groupby(
                        ['year', 'month'])[media].count().to_frame().reset_index()
                for index, row in dict_tmp[name].iterrows():
                    dict_df_names[name][str(row['month']) + "/" + str(row['year'])] = row[media]
    elif media == 'all_media':
        for name in list_names:
            if month_or_day == 'day':
                dict_df_names[name] = df_copy.loc[df_copy['from'] == name, :].groupby(['date'])[
                    'text'].count().to_frame().reset_index().sort_values(by='date')
                dict_df_names[name].columns = ['date', 'all_media']
            elif month_or_day == 'month':
                dict_df_names[name]: Dict[str, int] = {}
                dict_tmp[name]: Dict[pd.Series] = df_copy.loc[df_copy['from'] == name, :].groupby(['year', 'month'])[
                    'text'].count().to_frame().reset_index()
                dict_tmp[name].columns = ['year', 'month', 'all_media']
                for index, row in dict_tmp[name].iterrows():
                    dict_df_names[name][str(row['month']) + "/" + str(row['year'])] = row[media]
    else:
        for name in list_names:
            if month_or_day == 'day':
                dict_df_names[name] = \
                    df_copy.loc[(df_copy['from'] == name) & (df_copy[media] == 1),
                    :].groupby(['date'])[media].count().to_frame().reset_index().sort_values(by='date')
            elif month_or_day == 'month':
                dict_df_names[name]: Dict[str, int] = {}
                dict_tmp[name]: Dict[pd.Series] = \
                    df_copy.loc[(df_copy['from'] == name) & (df_copy[media] == 1),
                    :].groupby(['year', 'month'])[media].count().to_frame().reset_index()
                for index, row in dict_tmp[name].iterrows():
                    dict_df_names[name][str(row['month']) + "/" + str(row['year'])] = row[media]

                    # Viz
    name_x_axis: str = 'date'
    name_y_axis: str = 'number of {}'.format(dict_media[media] if media != 'all_media' else 'medias')
    name_graph: str = 'number of {} per person over time'.format(
        dict_media[media] if media != 'all_media' else 'medias')
    trace: dict = {}
    data: list = []

    if month_or_day == 'month':
        for name in list_names:
            trace[name] = go.Bar(name=name, x=list(dict_df_names[name].keys()), y=list(dict_df_names[name].values()),
                                 text=list(dict_df_names[name].values()), textposition="inside")
            data.append(trace[name])

    elif month_or_day == 'day':
        for name in list_names:
            trace[name] = go.Scatter(x=list(dict_df_names[name]['date']), y=list(dict_df_names[name][media]),
                                     mode='lines', name=name)
            data.append(trace[name])

    else:
        print("Not a valid argument")

    layout = go.Layout(template=color_graph()['template'], plot_bgcolor=color_graph()['plot_bgcolor'],
                       paper_bgcolor=color_graph()['paper_bgcolor'], barmode='group', xaxis=dict(title=name_x_axis),
                       yaxis=dict(title=name_y_axis), uniformtext_minsize=12, uniformtext_mode='hide')

    fig = go.Figure(data, layout)
    return fig

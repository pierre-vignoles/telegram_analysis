from datetime import time
from typing import List, Dict
import pandas as pd
import plotly.graph_objs as go

from python_script.basic_analysis.Viz import color_graph


def first_to_send_message(df: pd.DataFrame, list_names: List[str], time_limit: time, all_or_month: str) -> go.Figure:
    df_copy: pd.DataFrame = df.copy()
    df_copy['date'] = df_copy['datetime'].apply(lambda x: x.date())
    df_copy['time'] = df_copy['datetime'].apply(lambda x: x.time())
    df_copy = df_copy.loc[(df_copy['time'] >= time_limit), ['from', 'date', 'time']]

    df_time: pd.DataFrame = df_copy.groupby('date')['time', 'from'].first().reset_index()

    trace: dict = {}
    data: list = []

    if all_or_month == 'all':
        dict_count_by_name: Dict[str] = {}
        for name in list_names:
            dict_count_by_name[name]: Dict[str, int] = len(df_time.loc[df_time['from'] == name, :])

            # Graph
            trace[name] = go.Bar(name=name, x=[name], y=[dict_count_by_name[name]], text=[dict_count_by_name[name]], textposition="inside")
            data.append(trace[name])

        layout = go.Layout(template=color_graph()['template'], plot_bgcolor=color_graph()['plot_bgcolor'],
                           paper_bgcolor=color_graph()['paper_bgcolor'], uniformtext_minsize=20, uniformtext_mode='hide')
        fig = go.Figure(data, layout)

    elif all_or_month == 'month':

        dict_tmp: Dict[str] = {}
        dict_count_by_name: Dict[str] = {}
        df_time['month'] = df_time['date'].apply(lambda x: x.month)
        df_time['year'] = df_time['date'].apply(lambda x: x.year)
        for name in list_names:
            dict_tmp[name]: Dict[pd.Series] = df_time.loc[df_time['from'] == name].groupby(['year', 'month'])[
                'date'].count()
            dict_count_by_name[name]: Dict[str, int] = {}
            for index, value in dict_tmp[name].items():
                dict_count_by_name[name][str(index[1]) + "/" + str(index[0])] = value

                # Graph
            trace[name] = go.Bar(name=name, x=list(dict_count_by_name[name].keys()),
                                 y=list(dict_count_by_name[name].values()))
            data.append(trace[name])
            layout = go.Layout(template=color_graph()['template'], plot_bgcolor=color_graph()['plot_bgcolor'],
                               paper_bgcolor=color_graph()['paper_bgcolor'],uniformtext_minsize=12, uniformtext_mode='hide')

        fig = go.Figure(data, layout)

    return fig

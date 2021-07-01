from datetime import datetime
from typing import List, Dict
import pandas as pd
import plotly.graph_objs as go

from python_script.basic_analysis.Viz import color_graph


def function_messages_by_hour(df: pd.DataFrame, list_names: List[str], media: str, dict_media: Dict[str, str]) -> go.Figure:
    # Dict
    df_hour: Dict[str, datetime.hour] = {}
    list_hour: List[int] = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0, 1, 2, 3, 4]
    df_copy = df.copy()
    df_copy['hour'] = df_copy['datetime'].apply(lambda x: x.hour)
    for name in list_names:
        df_hour[name] = {}
        for hour in list_hour:
            if media == 'text':
                df_hour[name][hour] = df_copy.loc[(df_copy['hour'] == hour) & (df_copy["from"] == name) & (
                            df_copy["text"] != 'NaNValue'), 'hour'].count()
            elif media == 'all_media':
                df_hour[name][hour] = df_copy.loc[(df_copy['hour'] == hour) & (df_copy["from"] == name), 'hour'].count()
            else:
                df_hour[name][hour] = df_copy.loc[(df_copy['hour'] == hour) & (df_copy["from"] == name) & (df_copy[media] == 1), 'hour'].count()

    # Graph
    trace: dict = {}
    data: list = []
    for name in list_names:
        trace[name] = go.Bar(name=name, x=list(df_hour[name].keys()), y=list(df_hour[name].values()),
                             text=list(df_hour[name].values()), textposition='inside')
        data.append(trace[name])
    layout = go.Layout(template=color_graph()['template'], plot_bgcolor=color_graph()['plot_bgcolor'],
                       paper_bgcolor=color_graph()['paper_bgcolor'], barmode='stack', height=475, xaxis_title='Hours',
                       yaxis_title='number of {}'.format(dict_media[media] if media != 'all_media' else 'medias'))

    fig = go.Figure(data, layout)
    fig.update_xaxes(type='category', nticks=25, tickvals=list_hour)

    return fig

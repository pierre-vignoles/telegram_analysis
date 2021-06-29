from typing import List, Dict
import pandas as pd
import plotly.graph_objs as go

from Viz import color_graph


def graph_text_message_by_weekday(df: pd.DataFrame, list_names: List[str], media: str, dict_media: Dict[str, str]) -> go.Figure:

    list_weekdays_sort: List[str] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df_text_weekday: Dict[str] = {}
    for name in list_names:
        df_text_weekday[name] = {}
        for weekday in list_weekdays_sort:
            if media == 'text':
                df_text_weekday[name][weekday] = df.loc[
                    ((df["text"] != 'NaNValue') & (df["weekday"] == weekday) & (df["from"] == name)), 'weekday'].count()
            elif media == 'all_media':
                df_text_weekday[name][weekday] = df.loc[((df["weekday"] == weekday) & (df["from"] == name)), 'weekday'].count()
            else:
                df_text_weekday[name][weekday] = df.loc[(df["weekday"] == weekday) & (df["from"] == name) & (df[media] == 1), 'weekday'].count()

    # Graph
    trace: dict = {}
    data: list = []
    for name in list_names:
        trace[name] = go.Bar(name=name, x=list(df_text_weekday[name].keys()), y=list(df_text_weekday[name].values()),
                             text=list(df_text_weekday[name].values()), textposition='inside')
        data.append(trace[name])
    layout = go.Layout(template=color_graph()['template'], plot_bgcolor=color_graph()['plot_bgcolor'],
                       paper_bgcolor=color_graph()['paper_bgcolor'], barmode='stack', yaxis_title='number of {}'.format(dict_media[media] if media != 'all_media' else 'medias'))
    fig = go.Figure(data, layout)

    return fig

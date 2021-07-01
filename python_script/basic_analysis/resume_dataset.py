from datetime import datetime, timedelta
import pandas as pd
from typing import List, Dict
import plotly.graph_objs as go

from python_script.basic_analysis.Viz import color_graph


def graph_pie_repartition_medias(df: pd.DataFrame) -> go.Figure:
    list_medias: List[str] = ['text', 'media_type_video_file', 'media_type_photo', 'media_type_sticker']
    list_medias_clean: List[str] = ['Text', 'Video', 'Photo', 'Sticker']
    dict_medias_number: Dict[str, int] = {}
    for media in list_medias:
        if media == 'text':
            dict_medias_number[media] = len(df.loc[df['text'] != 'NaNValue'])
        else:
            dict_medias_number[media] = len(df.loc[df[media] == 1])

        fig = go.Figure(
            data=[go.Pie(labels=list_medias_clean, values=list(dict_medias_number.values()))]).update_layout(
            template=color_graph()['template'],
            plot_bgcolor=color_graph()['plot_bgcolor'],
            paper_bgcolor=color_graph()['paper_bgcolor'],
            height=115,
            margin=dict(l=10, r=20, t=0, b=0)).update_traces(hole=.6, textposition='inside')
        # Hide small label
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return fig


def graph_pie_number_messages(df: pd.DataFrame, list_names: List[str]) -> go.Figure:
    dict_number_media_per_person: Dict[str, int] = {}

    for name in list_names:
        dict_number_media_per_person[name] = len(df.loc[df['from'] == name])

    fig = go.Figure(data=[go.Pie(labels=list_names, values=list(dict_number_media_per_person.values()),
                                 textposition='inside')]).update_layout(template=color_graph()['template'],
                                                                        plot_bgcolor=color_graph()['plot_bgcolor'],
                                                                        paper_bgcolor=color_graph()['paper_bgcolor'],
                                                                        margin=dict(l=20, r=20, t=0,
                                                                                    b=0)).update_traces(hole=.6)

    return fig

def function_number_media(df: pd.DataFrame, media:str, dict_media: Dict[str, str]) -> str:
    if media == 'text':
        number_of_media: int = len(df.loc[df[media] != 'NaNValue'])
    elif media == 'all_media':
        number_of_media: int = len(df)
    else:
        number_of_media: int = len(df.loc[df[media] == 1])

    return "Number total of {} : {}".format(dict_media[media], number_of_media)


def function_one_message_every_x_seconds(df: pd.DataFrame, dict_media_singular: Dict[str, str], media: str) -> str:
    if media == 'text':
        timestamp_last_message: datetime = df['datetime'].max()
        timestamp_first_message: datetime = df['datetime'].min()
        timedelta_between_max_min_message: timedelta = timestamp_last_message - timestamp_first_message
        number_of_media: int = len(df.loc[df[media] != 'NaNValue'])
    elif media == 'all_media':
        timestamp_last_message: datetime = df['datetime'].max()
        timestamp_first_message: datetime = df['datetime'].min()
        timedelta_between_max_min_message: timedelta = timestamp_last_message - timestamp_first_message
        number_of_media: int = len(df)
    else:
        timestamp_last_message: datetime = df['datetime'].max()
        timestamp_first_message: datetime = df['datetime'].min()
        timedelta_between_max_min_message: timedelta = timestamp_last_message - timestamp_first_message
        number_of_media: int = len(df.loc[df[media] == 1])

    total_seconds_df: float = float(timedelta_between_max_min_message.total_seconds() / number_of_media)
    if total_seconds_df < 60:
        one_message_every_x_seconds = "1 {0} every {1} seconds".format(dict_media_singular[media], total_seconds_df)
    elif 3600 > total_seconds_df >= 60:
        one_message_every_x_seconds = "1 {0} every {1} minutes and {2} seconds".format(dict_media_singular[media],
                                                                                       int(total_seconds_df / 60),
                                                                                       round(total_seconds_df % 60))
    elif 86400 > total_seconds_df >= 3600:
        one_message_every_x_seconds = "1 {0} every {1} hours {2} minutes and {3} seconds".format(
            dict_media_singular[media], int(total_seconds_df / 3600), int((total_seconds_df % 3600) / 60),
            round((total_seconds_df % 3600) % 60))
    elif total_seconds_df >= 86400:
        one_message_every_x_seconds = "1 {0} every {1} days {2} hours {3} minutes and {4} seconds".format(
            dict_media_singular[media], int(total_seconds_df / 86400), int((total_seconds_df % 86400) / 3600),
            int(((total_seconds_df % 86400) % 3600) / 60), round(((total_seconds_df % 86400) % 3600) % 60))

    return one_message_every_x_seconds


def function_time_df(df: pd.DataFrame) -> str:
    timestamp_last_message: datetime = df['datetime'].max()
    timestamp_first_message: datetime = df['datetime'].min()
    timedelta_between_max_min_message: timedelta = timestamp_last_message - timestamp_first_message
    if timedelta_between_max_min_message.days < 30:
        string_timedelta_between_max_min_message: str = "{0} days".format(timedelta_between_max_min_message.days)
    elif 365 > timedelta_between_max_min_message.days >= 30:
        string_timedelta_between_max_min_message: str = "{0} months and {1} days".format(
            int(timedelta_between_max_min_message.days / 30), round(timedelta_between_max_min_message.days % 30))
    elif timedelta_between_max_min_message.days >= 365:
        string_timedelta_between_max_min_message: str = "{0} year {1} months and {2} days".format(
            int(timedelta_between_max_min_message.days / 365), int((timedelta_between_max_min_message.days % 365) / 30),
            round((timedelta_between_max_min_message.days % 365) % 30))
    return string_timedelta_between_max_min_message

from typing import Dict, List
import pandas as pd
import plotly.graph_objs as go

from Viz import color_graph


def find_top_stickers_used_dash(df: pd.DataFrame, top_number: int, all_or_month: str, list_names: List[str]):
    df_copy: pd.DataFrame = df.copy()

    dict_df_names: Dict[str] = {}

    # Graph
    name_y_axis: str = 'number of stickers'
    trace: dict = {}
    data: list = []

    if all_or_month == 'all':
        for name in list_names:
            dict_df_names[name]: Dict[str] = {}
            dict_df_names[name]['path'] = list(df_copy.loc[
                                                   (df_copy['from'] == name) & (df_copy['media_type_sticker'] == 1) & (
                                                           df_copy['file'].str.contains(
                                                               '.tgs') == False), 'file'].value_counts()[
                                               :int(top_number)].keys())
            dict_df_names[name]['count_stickers'] = len(df_copy.loc[(df_copy['from'] == name) & (
                    df_copy['media_type_sticker'] == 1) & (df_copy['file'].str.contains('.tgs') == False), 'file'])

            new_list_path = []
            for path in dict_df_names[name]['path']:
                new_list_path.append(str(path) + "_thumb.jpg")
            dict_df_names[name]['path'] = new_list_path

            trace[name] = go.Bar(name=name, x=[name], y=[dict_df_names[name]['count_stickers']],
                                 text=[dict_df_names[name]['count_stickers']], textposition="inside")
            data.append(trace[name])
            layout = go.Layout(yaxis=dict(title=name_y_axis), title=dict(text='Click on a bar of the graph to show '
                                                                               'images'),
                               uniformtext_minsize=20,
                               uniformtext_mode='hide',
                               template=color_graph()['template'],
                               plot_bgcolor=color_graph()['plot_bgcolor'],
                               paper_bgcolor=color_graph()['paper_bgcolor'])

    elif all_or_month == 'month':
        df_copy['date'] = df_copy['datetime'].apply(lambda x: x.date())
        df_copy['month'] = df_copy['datetime'].apply(lambda x: x.month)
        df_copy['year'] = df_copy['datetime'].apply(lambda x: x.year)
        name_x_axis: str = 'date'

        for name in list_names:
            dict_df_names[name]: pd.DataFrame = df_copy.loc[
                                                (df_copy['from'] == name) & (df_copy['media_type_sticker'] == 1) & (
                                                        df_copy['file'].str.contains('.tgs') == False), :].groupby(
                ['year', 'month'])['file'].count().to_frame().reset_index()
            dict_df_names[name]['path'] = dict_df_names[name].apply(lambda x:
                                                                    list(df_copy.loc[
                                                                             (df_copy['media_type_sticker'] == 1) & (
                                                                                     df_copy['from'] == name) & (
                                                                                     df_copy['month'] == x[
                                                                                 'month']) & (df_copy['year'] == x[
                                                                                 'year']) & (
                                                                                     df_copy['file'].str.contains(
                                                                                         '.tgs') == False), 'file'].value_counts()[
                                                                         :int(top_number)].keys()), axis=1)

            dict_df_names[name]['year_month'] = dict_df_names[name].apply(
                lambda x: str(x['month']) + "/" + str(x['year']), axis=1)
            dict_df_names[name] = dict_df_names[name].drop(['year', 'month'], axis=1)

            for i in range(0, len(dict_df_names[name]['path'])):
                new_list_path = []
                for path in dict_df_names[name]['path'][i]:
                    new_list_path.append(str(path) + "_thumb.jpg")
                dict_df_names[name]['path'][i] = new_list_path

            trace[name] = go.Bar(name=name, x=list(dict_df_names[name]['year_month']),
                                 y=list(dict_df_names[name]['file']),
                                 text=list(dict_df_names[name]['file']), textposition="inside")
            data.append(trace[name])
            layout = go.Layout(yaxis=dict(title=name_y_axis), title=dict(text='Click on a bar of the graph to show '
                                                                               'images'),
                               uniformtext_minsize=12,
                               uniformtext_mode='hide',
                               template=color_graph()['template'],
                               plot_bgcolor=color_graph()['plot_bgcolor'],
                               paper_bgcolor=color_graph()['paper_bgcolor'])

    fig = go.Figure(data, layout)

    return fig, dict_df_names

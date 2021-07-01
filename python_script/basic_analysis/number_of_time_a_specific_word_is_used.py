from typing import Dict
import pandas as pd
import plotly.graph_objs as go

from python_script.basic_analysis.Viz import color_graph


def find_number_of(df: pd.DataFrame, symbol: str, list_names: list, all_or_month_or_day: str) -> go.Figure:
    df_copy: pd.DataFrame = df.copy()
    df_copy['date'] = df_copy['datetime'].apply(lambda x: x.date())
    df_copy['month'] = df_copy['datetime'].apply(lambda x: x.month)
    df_copy['year'] = df_copy['datetime'].apply(lambda x: x.year)

    # If the string wrote by the user start by '\'
    if symbol[0] == "/":
        regex_string = symbol[1:]
    # Transform the string into a list and delete na values
    else:
        symbol_list = symbol.split(",")
        symbol_list = list(filter(None, symbol_list))
        regex_string: str = ""

    # Create the regex
    # If the string wrote by the user do not start by '\'
    if symbol[0] != "/":
        for index, element in enumerate(symbol_list):
            if len(symbol_list) > 1:
                if (index + 1) == len(symbol_list):
                    regex_string = regex_string + "({}\\b)".format(element)
                else:
                    regex_string = regex_string + "({}\\b)|".format(element)
            else:
                regex_string = regex_string + "({}\\b)".format(element)

    dict_df_names: Dict[str] = {}
    for name in list_names:
        if all_or_month_or_day == 'all':
            dict_df_names[name] = len(df_copy.loc[(df_copy['text'].str.contains(regex_string, case=False, na=False)) & (
                    df_copy['from'] == name), ['text']])
        elif all_or_month_or_day == 'month':
            dict_tmp: Dict[str] = {}
            dict_df_names[name]: Dict[str, int] = {}
            dict_tmp[name] = df_copy.loc[
                (df_copy['text'].str.contains(regex_string, case=False, na=False)) & (df_copy['from'] == name), ['text',
                                                                                                                 'year',
                                                                                                                 'month']].groupby(
                ['year', 'month'])['text'].count()
            for index, value in dict_tmp[name].items():
                dict_df_names[name][str(index[1]) + "/" + str(index[0])] = value
        elif all_or_month_or_day == 'day':
            dict_df_names[name] = df_copy.loc[
                (df_copy['text'].str.contains(regex_string, case=False, na=False)) & (df_copy['from'] == name), ['date',
                                                                                                                 'text']].groupby(
                ['date'])['text'].count().to_dict()

    # Graph
    if symbol[0] == "/":
        name_y_axis: str = "number of {}".format(symbol[1:])
    else:
        name_y_axis: str = "number of '{}'".format(symbol)

    if all_or_month_or_day == 'all':
        trace: dict = {}
        data: list = []
        for name in list_names:
            trace[name] = go.Bar(name=name, x=[name], y=[dict_df_names[name]], text=[dict_df_names[name]],
                                 textposition="inside")
            data.append(trace[name])
        layout = go.Layout(yaxis_title=name_y_axis, template=color_graph()['template'],
                          plot_bgcolor=color_graph()['plot_bgcolor'],
                          paper_bgcolor=color_graph()['paper_bgcolor'], uniformtext_minsize=20, uniformtext_mode='hide')
        fig = go.Figure(data, layout)

    if all_or_month_or_day == 'month':
        trace: dict = {}
        data: list = []
        for name in list_names:
            trace[name] = go.Bar(name=name, x=list(dict_df_names[name].keys()),
                                 y=list(dict_df_names[name].values()), textposition="inside")
            data.append(trace[name])
        layout = go.Layout(yaxis_title=name_y_axis, template=color_graph()['template'],
                           plot_bgcolor=color_graph()['plot_bgcolor'],
                           paper_bgcolor=color_graph()['paper_bgcolor'], uniformtext_minsize=12,
                           uniformtext_mode='hide')
        fig = go.Figure(data, layout)

    if all_or_month_or_day == 'day':
        trace: dict = {}
        data: list = []
        for name in list_names:
            trace[name] = go.Scatter(mode='lines', name=name, x=list(dict_df_names[name].keys()),
                                     y=list(dict_df_names[name].values()))
            data.append(trace[name])
        layout = go.Layout(yaxis_title=name_y_axis, template=color_graph()['template'],
                           plot_bgcolor=color_graph()['plot_bgcolor'],
                           paper_bgcolor=color_graph()['paper_bgcolor'])
        fig = go.Figure(data, layout)

    return fig

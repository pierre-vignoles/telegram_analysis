from typing import List, Dict
import pandas as pd
import plotly.graph_objs as go

from python_script.basic_analysis.Viz import color_graph


def graph_analyse_sentiments(df: pd.DataFrame, all_or_month_or_weekday: str, name_choose: str,
                             list_names: List[str]) -> go.Figure:
    dict_df_names: Dict[str] = {}
    dict_tmp: Dict[str] = {}
    trace: dict = {}
    data: list = []

    if name_choose == 'all':
        if all_or_month_or_weekday == 'all':
            dict_df_names = df.groupby(['sentiment'])['sentiment'].count()
            for sentiment in df['sentiment'].unique():
                trace[sentiment] = go.Bar(name=sentiment, x=[sentiment], y=[dict_df_names[sentiment]], text=[dict_df_names[sentiment]], textposition='inside')
                data.append(trace[sentiment])

        elif all_or_month_or_weekday == 'month':
            dict_tmp = df.groupby(['sentiment', 'year', 'month'])['sentiment'].count()
            for sentiment in df['sentiment'].unique():
                dict_df_names[sentiment]: Dict[str, int] = {}
                for index, value in dict_tmp[sentiment].items():
                    dict_df_names[sentiment][str(index[1]) + "/" + str(index[0])] = value
                trace[sentiment] = go.Bar(name=sentiment, x=list(dict_df_names[sentiment].keys()),
                                          y=list(dict_df_names[sentiment].values()), text=list(dict_df_names[sentiment].values()), textposition='inside')
                data.append(trace[sentiment])

        elif all_or_month_or_weekday == 'weekday':
            dict_df_names = df.groupby(['sentiment', 'weekday'])['sentiment'].count()
            for sentiment in df['sentiment'].unique():
                trace[sentiment] = go.Bar(name=sentiment, x=list(dict_df_names[sentiment].keys()),
                                          y=list(dict_df_names[sentiment].values), text=list(dict_df_names[sentiment].values), textposition='inside')
                data.append(trace[sentiment])

    elif name_choose == 'comparison':
        for name in list_names:
            dict_df_names[name] = df.loc[df['from'] == name, :].groupby(['sentiment'])['sentiment'].count()
            # Graph
            trace[name] = go.Bar(name=name, x=list(dict_df_names[name].keys()), y=list(dict_df_names[name].values), text=list(dict_df_names[name].values), textposition='inside')
            data.append(trace[name])

    else:
        if all_or_month_or_weekday == 'all':
            dict_df_names = df.loc[df['from'] == name_choose, :].groupby(['sentiment'])['sentiment'].count()
            for sentiment in df['sentiment'].unique():
                trace[sentiment] = go.Bar(name=sentiment, x=[sentiment], y=[dict_df_names[sentiment]], text=[dict_df_names[sentiment]], textposition='inside')
                data.append(trace[sentiment])

        elif all_or_month_or_weekday == 'month':
            dict_tmp = df.loc[df['from'] == name_choose, :].groupby(['sentiment', 'year', 'month'])['sentiment'].count()
            for sentiment in df['sentiment'].unique():
                dict_df_names[sentiment]: Dict[str, int] = {}
                for index, value in dict_tmp[sentiment].items():
                    dict_df_names[sentiment][str(index[1]) + "/" + str(index[0])] = value
                trace[sentiment] = go.Bar(name=sentiment, x=list(dict_df_names[sentiment].keys()),
                                          y=list(dict_df_names[sentiment].values()), text=list(dict_df_names[sentiment].values()), textposition='inside')
                data.append(trace[sentiment])

        elif all_or_month_or_weekday == 'weekday':
            dict_df_names = df.loc[df['from'] == name_choose, :].groupby(['sentiment', 'weekday'])['sentiment'].count()
            for sentiment in df['sentiment'].unique():
                trace[sentiment] = go.Bar(name=sentiment, x=list(dict_df_names[sentiment].keys()),
                                          y=list(dict_df_names[sentiment].values), text=list(dict_df_names[sentiment].values), textposition='inside')
                data.append(trace[sentiment])

    layout = go.Layout(barmode='group', template=color_graph()['template'], plot_bgcolor=color_graph()['plot_bgcolor'],
                       paper_bgcolor=color_graph()['paper_bgcolor'], uniformtext_minsize=12, uniformtext_mode='hide')
    fig = go.Figure(data, layout)

    return fig


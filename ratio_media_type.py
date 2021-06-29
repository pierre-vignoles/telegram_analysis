from datetime import date

from emoji import UNICODE_EMOJI
import pandas as pd

from plotly.subplots import make_subplots
import plotly.graph_objs as go

from Viz import color_graph


def text_has_emoji(text: str) -> bool:
    for character in text:
        if character in UNICODE_EMOJI['en']:
            return True
    return False


def function_ratio_media_type(df: pd.DataFrame, list_names: list):
    df_media: dict = {}
    list_media_type_tmp: list = ['text', 'animation', 'phone_call', 'photo', 'sticker', 'video_file', 'voice_message',
                                 'link']
    list_media_type: list = []
    for column in list_media_type_tmp:
        if column in df.columns:
            list_media_type.append(column)
        elif "media_type_" + str(column) in df.columns:
            list_media_type.append(column)
    df_copy: pd.DataFrame = df.copy()
    df_copy['text'] = df_copy['text'].apply(lambda x: str(x))
    df_copy['emoji'] = df_copy['text'].apply(lambda x: text_has_emoji(x))
    if True in df_copy['emoji']:
        list_media_type.append('emoji')

    # Dict
    for media in list_media_type:
        df_media[media] = {}
        for name in list_names:
            if media == 'text':
                df_media[media][name] = df_copy.loc[
                    (df_copy['text'] != 'NaNValue') & (df_copy['from'] == name), media].count()
            elif media == 'emoji':
                df_media[media][name] = df_copy.loc[
                    (df_copy['emoji'] == True) & (df_copy['from'] == name), media].count()
            else:
                df_media[media][name] = df_copy.loc[
                    (df_copy["media_type_" + media] == 1) & (df_copy['from'] == name), "media_type_" + media].count()

    # Graph
    if len(list_media_type) == 9:
        specs = [[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}],
                 [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}],
                 [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]]
        rows = 3
        cols = int(len(list_media_type) / rows)
    elif len(list_media_type) == 8:
        specs = [[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}],
                 [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]]
        rows = 2
        cols = int(len(list_media_type) / rows)
    elif len(list_media_type) == 7:
        specs = [[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}],
                 [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]]
        rows = 2
        cols = int((len(list_media_type) + 1) / rows)
    elif len(list_media_type) == 6:
        specs = [[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}],
                 [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]]
        rows = 2
        cols = int(len(list_media_type) / rows)

    labels = list_names
    fig = make_subplots(rows=rows, cols=cols, specs=specs,
                        subplot_titles=[media.replace('_', ' ') for media in list_media_type])

    for index, media in enumerate(list_media_type):
        row = (int(index / cols) + 1)
        col = ((index % cols) + 1)
        fig.add_trace(go.Pie(labels=labels, values=list(df_media[media].values()), name=media), row, col)

    fig.update_traces(hole=.6)

    fig.update_layout(template=color_graph()['template'], plot_bgcolor=color_graph()['plot_bgcolor'],
                      paper_bgcolor=color_graph()['paper_bgcolor'], margin=dict(l=20, r=20, t=20, b=20))

    return fig

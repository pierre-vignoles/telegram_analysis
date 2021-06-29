import base64

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_auth

from dash.dependencies import Input, Output, State

from typing import Tuple, List, Dict
from datetime import datetime, time
import pandas as pd
import plotly.graph_objs as go
from io import BytesIO

# from Viz import encode_image
from data_prep import upload_json
from first_to_send_message import first_to_send_message
from messages_send_by_weekday import graph_text_message_by_weekday
from number_of_time_a_specific_word_is_used import find_number_of
from resume_dataset import function_one_message_every_x_seconds, function_time_df, graph_pie_repartition_medias, \
    function_number_media
from ratio_media_type import function_ratio_media_type
from messages_send_by_hour import function_messages_by_hour
from messages_over_time import function_number_of
from sentiment_analyse.data_prep_nlp import data_prep_nlp
from sentiment_analyse.viz_nlp import graph_analyse_sentiments
from show_stickers import find_top_stickers_used_dash
from sentiment_analyse.wordcloud_function import wordcloud_most_used_word


def min_max_dates(df: pd.DataFrame) -> Tuple[datetime, datetime]:
    if df is not None:
        min_date: datetime = df['datetime'].min()
        max_date: datetime = df['datetime'].max()
    else:
        min_date: datetime = datetime(2000, 1, 1)
        max_date: datetime = datetime(2000, 1, 1)
    return min_date, max_date


def drawFigure(name_id: str):
    return dbc.Spinner(children=[
        html.Div([
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(id=name_id)
                ]),
                className=["h-100 d-inline-block", "w-100 p-3"]
            ),
        ])
    ], color='info')


def drawFigure_with_radio_item(name_id_figure: str, name_id_radio_item: str, dict_label_value: Dict[str, str]):
    return dbc.Spinner(children=[
        html.Div([
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(id=name_id_figure),
                    dbc.RadioItems(
                        id=name_id_radio_item,
                        options=[{'label': label_value[0], 'value': label_value[1]} for i, label_value in
                                 enumerate(dict_label_value.items())],
                        value=list(dict_label_value.values())[0],
                        inline=True,
                        style={'margin-left': '45%'},
                    )
                ]),
                className=["h-100 d-inline-block", "w-100 p-3"]
            )
        ])
    ], color='info')


# Text field
def drawText(text: str):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2(text),
                ], style={'textAlign': 'center'})
            ])
        ),
    ])


def generate_image(image, style):
    return html.Div([
        html.A([
            html.Img(
                src=image,
                style=style
            )
        ])
    ])


def function_tab_1(dict_media: Dict[str, str], df=None):
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H3('Select start and end dates :')
                            ], width=5),
                            dbc.Col([
                                dcc.DatePickerRange(
                                    id='my_date_picker',
                                    min_date_allowed=min_max_dates(df)[0],
                                    max_date_allowed=min_max_dates(df)[1],
                                    start_date=min_max_dates(df)[0],
                                    end_date=min_max_dates(df)[1]
                                )
                            ], width=5)
                        ], align='center'),

                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                html.H3('Select the media type :')
                            ], width=5),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="dropdown_media",
                                    options=[
                                        {"label": dict_media["all_media"], "value": "all_media"},
                                        {"label": dict_media["text"], "value": 'text'},
                                        {"label": dict_media["media_type_photo"], "value": 'media_type_photo'},
                                        {"label": dict_media["media_type_video_file"],
                                         "value": 'media_type_video_file'},
                                        {"label": dict_media["media_type_sticker"],
                                         "value": 'media_type_sticker'},
                                        {"label": dict_media["media_type_voice_message"],
                                         "value": 'media_type_voice_message'},
                                        {"label": dict_media["media_type_phone_call"],
                                         "value": 'media_type_phone_call'},
                                        {"label": dict_media["media_type_audio_file"],
                                         "value": 'media_type_audio_file'},
                                        {"label": dict_media["media_type_animation"],
                                         "value": 'media_type_animation'},
                                        {"label": dict_media["media_type_emoji"], "value": 'media_type_emoji'},
                                        {"label": dict_media["media_type_link"], "value": 'media_type_link'},
                                    ],
                                    value='all_media'
                                ),
                            ], width=5),
                            dbc.Col([
                                dbc.Button("Submit", className="btn btn-primary",
                                           id='submit_button', size="lg")
                            ], width=2)
                        ], align='center')
                    ]),
                    className=["h-100 d-inline-block", "w-100 p-3"]
                )
            ], width=6),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div(id='dataset_stats',
                                         style={'fontSize': 20}
                                         )
                            ], width=7),
                            dbc.Col([
                                dbc.Spinner(children=[dcc.Graph(id='graph_repartition_media')], color='info')
                            ], width=5)
                        ], align='center')
                    ]),
                    className=["h-auto d-inline-block", "w-100 p-3"]
                )
            ], width=6)
        ], align='center'),
        html.Br(),
        dbc.Row([
            dbc.Col([
                drawText('Media send by weekday')
            ], width=4),
            dbc.Col([
                drawText('Proportion of different medias send per person')
            ], width=8)
        ], align='center'),
        dbc.Row([
            dbc.Col([
                drawFigure('graph_text_message_by_weekday')
            ], width=4),
            dbc.Col([
                drawFigure('graph_proportion_media')
            ], width=8)
        ], align='stretch'),

        html.Br(),
        dbc.Row([
            dbc.Col([
                drawText('Media send by hour')
            ], width=4),
            dbc.Col([
                drawText('Evolution of the number of medias send per person')
            ], width=8)
        ], align='center'),
        dbc.Row([
            dbc.Col([
                drawFigure('graph_messages_send_by_hour')
            ], width=4),
            dbc.Col([
                drawFigure_with_radio_item('graph_messages_send_per_day_month',
                                           'radio_item_medias_send_per_day_month',
                                           {"Day": "day", "Month": "month"})
            ], width=8)
        ], align='stretch'),

        html.Br(),
        dbc.Row([
            dbc.Col([
                drawText('First to send message')
            ], width=6),
            dbc.Col([
                drawText('Utilisation of a specific word')
            ], width=6),
        ], align='center'),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H3("Choose the start time of a day :")
                            ], width=6),
                            dbc.Col([
                                dbc.Input(type='time', id="time_picker", value="05:15",
                                          style={'width': '50%'})
                            ], width=4),
                            dbc.Col([
                                dbc.Button("Go", color="info", className="mr-1",
                                           id='submit_button_first_to_send_message', size="lg")
                            ], width=2)
                        ], align='center')
                    ]),
                    className=["h-100 d-inline-block", "w-100 p-3"]
                )
            ], width=6),
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H3("Choose a word or a list of words split by ',' :")
                            ], width=6),
                            dbc.Col([
                                dbc.Input(id="word_picker", placeholder="Write a word...", type="text",
                                          value="test", className="form-control"),
                            ], width=3),
                            dbc.Col([
                                dbc.Button("Go", color="info", className="mr-1",
                                           id='submit_button_utilisation_of_a_specific_word', size="lg")
                            ], width=1),
                            dbc.Col([
                                dbc.Button(
                                    "Info", id="button_info_regex", color="danger", outline=False,
                                    className="mr-1",
                                    n_clicks=0, size="lg"
                                ),
                                dbc.Popover(
                                    children=[dbc.PopoverHeader("Regex info"),
                                              dbc.PopoverBody(html.P(["Start your regex with the symbol '/'",
                                                                      html.Br(),
                                                                      r"Double your backslash '\' if you need to use it"
                                                                      ])
                                                              ),
                                              ],
                                    id="hover_description_info_regex",
                                    target="button_info_regex",
                                    trigger="hover",
                                )
                            ], width=1)

                        ], align='center')
                    ]),
                    className=["h-auto d-inline-block", "w-100 p-3"]
                )
            ], width=6)
        ], align='stretch'),
        dbc.Row([
            dbc.Col([
                drawFigure_with_radio_item("graph_first_to_send_message", "radio_items_all_or_month",
                                           {"All": "all", "By month": "month"})
            ], width=6),
            dbc.Col([
                drawFigure_with_radio_item("graph_number_of_specific_word", "radio_items_day_month_all",
                                           {"All": "all", "By month": "month", "By day": "day"})
            ], width=6)
        ], align='stretch'),

        html.Br(),
        dbc.Row([
            dbc.Col([
                drawText("Most stickers used per person")
            ], width=12)
        ], align='center'),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H3("Choose the number of stickers you want to show :  5 ",
                                id="show_number_of_stickers"),
                        html.Br(),
                        # dcc.Slider(id="slider_number_stickers", min=1, max=10, step=1, value=5,
                        #            marks={number: number for number in range(1, 11)}, className='mt-4')
                        dbc.Input(type="range", id="slider_number_stickers", min=1, max=10, step=1,
                                  value=5, style={'width': '70%', 'margin-left': '15%'}, className="form-group")
                    ]),
                    className=["h-100 d-inline-block", "w-100 p-3"]
                )
            ], width=6),
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H3("Upload all the stickers images : "),
                        html.Br(),
                        dcc.Upload(
                            id='upload_stickers',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Click here')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            multiple=True
                        ),
                    ]),
                    className=["h-auto d-inline-block", "w-100 p-3"]
                )
            ], width=6)
        ], align='stretch', no_gutters=True),
        dbc.Row([
            dbc.Col([
                drawFigure_with_radio_item("graph_show_stickers", "radio_items_all_or_month_stickers",
                                           {"All": "all", "By month": "month"})
            ], width=6),
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        dbc.Spinner(children=[html.Div(id="img_stickers")], spinnerClassName="spinner",
                                    type=None)
                    ]),
                    className=["h-auto d-inline-block", "w-100 p-3"]
                )
            ], width=6)
        ], align='stretch', no_gutters=True)
    ])


def function_tab_2(list_names=None):
    if list_names is None:
        list_names = ['name1', 'name2']
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H2("Click on the button to launch the data prep : "),
                            ], width=9),
                            dbc.Col([
                                dbc.Button("Data Prep", className="btn btn-primary", id='data_prep_nlp_button',
                                           size="lg",
                                           n_clicks=0)
                            ], width=2),
                            dbc.Col([
                                dbc.Spinner(
                                    children=[html.Div(id='data_prep_nlp_empty_div', style={'display': 'none'})])
                            ], width=1),
                        ]),
                    ]),
                    className=["h-auto d-inline-block", "w-100 p-3"]
                )
            ], width=6),
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H2("Then choose the option you want for the Viz : "),
                            ], width=9),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="dropdown_name_nlp",
                                    options=[{"label": name, "value": name} for name in list_names] +
                                            [{"label": "Everyone", "value": "all"},
                                             {"label": "Comparison", "value": 'comparison'}],
                                    value='all'
                                )
                            ], width=3),
                        ]),
                    ]),
                    className=["h-100 d-inline-block", "w-100 p-3"]
                )
            ], width=6)
        ], align='stretch'),
        html.Br(),
        dbc.Row([
            dbc.Col([
                drawText("Sentiments analysis (TextBlob)")
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                drawFigure_with_radio_item("graph_nlp", "nlp_radio_items_all_or_month_or_weekday",
                                           {"All": "all", "By month": "month", "Weekday": "weekday"})
            ], width=12),
        ]),

        html.Br(),
        dbc.Row([
            dbc.Col([
                drawText("Most used words")
            ], width=12)
        ], align='center'),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H3("Choose the number of words you want to show :  5 ",
                                id="show_number_of_words_wordcloud"),
                        html.Br(),
                        dbc.Input(type="range", id="slider_number_words_wordcloud", min=5, max=200, step=5,
                                  value=100, style={'width': '70%', 'margin-left': '15%'}, className="form-group")
                    ]),
                )
            ], width=12),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        dbc.Spinner(children=[html.Div(id="img_wordcloud")], spinnerClassName="spinner",
                                    type=None)
                    ])
                )
            ], width=12)
        ])
    ])


def run_dash(dict_media: Dict[str, str], dict_media_singular: Dict[str, str]) -> dash:
    external = [dbc.themes.SLATE]
    USERNAME_PASSWORD_PAIRS = [['username', 'password'], ['admin', 'admin']]

    app = dash.Dash(__name__, external_stylesheets=external)
    server = app.server
    auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
    # app.config['suppress_callback_exceptions'] = True

    # Layout
    app.layout = html.Div(children=[
        dbc.Card([
            dbc.Row([
                dbc.Col([
                    # dbc.Nav(
                    #     className="navbar navbar-expand-lg navbar-dark bg-primary",
                    #     children=[dbc.NavbarBrand("Telegram")],
                    #     id="card_tabs",
                    #     card=True
                    # )
                    html.Br(),
                    dbc.Col([
                        html.H1("Telegram")
                    ], width=3),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Tabs([
                                dbc.Tab(label="Basic analyse", tab_id="tab_1"),
                                dbc.Tab(label="Sentiments analyses", tab_id="tab_2"),
                            ],
                                id="card_tabs",
                                card=True,
                                active_tab="tab_1",
                            )
                        ], width=3),
                        dbc.Col([
                            dcc.Upload(
                                id='upload_dataset',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Click here'),
                                    ' to upload your conversation.'
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                multiple=True
                            ),
                        ], width=4),
                        dbc.Col([
                            dbc.Spinner(children=[html.Div(id='spinner_data_prep')])
                        ], width=1),
                        dbc.Col([
                            dbc.Button("Launch the Viz", className="btn btn-primary", id='data_prep_button', size="lg",
                                       n_clicks=0)
                        ], width=3)
                    ], align='center')
                ], width=12)
            ]),
            html.Br(),
            dbc.CardBody(id="graph_tab", className="card-text")

        ], color='dark')
    ])

    @app.callback(Output('spinner_data_prep', 'children'),
                  [Input('upload_dataset', 'contents')],
                  State('upload_dataset', 'filename')
                  )
    def spinner_data_prep(contents, filename):
        if contents is not None:
            global df, list_names
            df = upload_json(contents, filename)
            # List of the name of person in the dataset
            list_names = df['from'].unique()

    @app.callback(Output('data_prep_button', 'disabled'),
                  [Input('upload_dataset', 'contents'),
                   Input("card_tabs", "active_tab")]
                  )
    def disable_button_launch_viz(contents, active_tab):
        if contents is None:
            return True
        else:
            if active_tab == 'tab_2':
                return True
            else:
                False

    @app.callback(Output("graph_tab", "children"),
                  [Input("card_tabs", "active_tab"),
                   Input("data_prep_button", "n_clicks")],
                  State('upload_dataset', 'contents')
                  )
    def update_dataset_tab(active_tab, n_clicks, contents):
        if contents is not None:
            if active_tab == 'tab_1':
                return function_tab_1(dict_media, df)
            elif active_tab == 'tab_2':
                return function_tab_2(list_names)
        else:
            print("No file")
            if active_tab == 'tab_1':
                return function_tab_1(dict_media)
            elif active_tab == 'tab_2':
                return function_tab_2()

    # Messages send per day
    @app.callback(Output('graph_text_message_by_weekday', 'figure'),
                  [Input('submit_button', 'n_clicks')],
                  [State('my_date_picker', 'start_date'),
                   State('my_date_picker', 'end_date'),
                   State('dropdown_media', 'value'),
                   State('upload_dataset', 'contents')]
                  )
    def update_messages_by_weekday(n_clicks, start_date: datetime, end_date: datetime, media: str,
                                   contents) -> go.Figure:
        if contents is not None:
            df_new: pd.DataFrame = df.loc[(df['datetime'] <= end_date) & (df['datetime'] >= start_date), :]
            return graph_text_message_by_weekday(df_new, list_names, media, dict_media)
        else:
            return dash.no_update

    # Number total of messages
    @app.callback(Output('dataset_stats', 'children'),
                  [Input('submit_button', 'n_clicks')],
                  [State('my_date_picker', 'start_date'),
                   State('my_date_picker', 'end_date'),
                   State('dropdown_media', 'value'),
                   State('upload_dataset', 'contents')]
                  )
    def update_number_total_messages(n_clicks, start_date: datetime, end_date: datetime, media: str, contents) -> str:
        if contents is not None:
            df_new: pd.DataFrame = df.loc[(df['datetime'] <= end_date) & (df['datetime'] >= start_date), :]
            stats = html.P([function_number_media(df_new, media, dict_media), html.Br(),
                            "Period : {}".format(function_time_df(df_new)), html.Br(),
                            "{}".format(function_one_message_every_x_seconds(df_new, dict_media_singular, media))])
            return stats
        else:
            return dash.no_update

    @app.callback(Output('graph_repartition_media', 'figure'),
                  [Input('submit_button', 'n_clicks')],
                  [State('my_date_picker', 'start_date'),
                   State('my_date_picker', 'end_date'),
                   State('upload_dataset', 'contents')]
                  )
    def update_graph_number_message_per_person(n_clicks, start_date: datetime, end_date: datetime,
                                               contents) -> go.Figure:
        if contents is not None:
            df_new: pd.DataFrame = df.loc[(df['datetime'] <= end_date) & (df['datetime'] >= start_date), :]
            return graph_pie_repartition_medias(df_new)
        else:
            return dash.no_update

    @app.callback(Output('graph_proportion_media', 'figure'),
                  [Input('submit_button', 'n_clicks')],
                  [State('my_date_picker', 'start_date'),
                   State('my_date_picker', 'end_date'),
                   State('upload_dataset', 'contents')]
                  )
    def update_graph_proportion_media(n_clicks, start_date: datetime, end_date: datetime, contents) -> go.Figure:
        if contents is not None:
            df_new: pd.DataFrame = df.loc[(df['datetime'] <= end_date) & (df['datetime'] >= start_date), :]
            return function_ratio_media_type(df_new, list_names)
        else:
            return dash.no_update

    @app.callback(Output('graph_messages_send_by_hour', 'figure'),
                  [Input('submit_button', 'n_clicks')],
                  [State('my_date_picker', 'start_date'),
                   State('my_date_picker', 'end_date'),
                   State('dropdown_media', 'value'),
                   State('upload_dataset', 'contents')]
                  )
    def update_messages_by_hour(n_clicks, start_date: datetime, end_date: datetime, media: str, contents) -> go.Figure:
        if contents is not None:
            df_new: pd.DataFrame = df.loc[(df['datetime'] <= end_date) & (df['datetime'] >= start_date), :]
            return function_messages_by_hour(df_new, list_names, media, dict_media)
        else:
            return dash.no_update

    @app.callback(Output('graph_messages_send_per_day_month', 'figure'),
                  [Input('submit_button', 'n_clicks'),
                   Input('radio_item_medias_send_per_day_month', 'value')],
                  [State('my_date_picker', 'start_date'),
                   State('my_date_picker', 'end_date'),
                   State('dropdown_media', 'value'),
                   State('upload_dataset', 'contents')]
                  )
    def update_media_by_day_month(n_clicks, month_or_day: str, start_date: datetime, end_date: datetime,
                                  media: str, contents) -> go.Figure:
        if contents is not None:
            df_new: pd.DataFrame = df.loc[(df['datetime'] <= end_date) & (df['datetime'] >= start_date), :]
            return function_number_of(df_new, media, list_names, month_or_day, dict_media)
        else:
            return dash.no_update

    @app.callback(Output('graph_first_to_send_message', 'figure'),
                  [Input('submit_button_first_to_send_message', 'n_clicks'),
                   Input('submit_button', 'n_clicks'),
                   Input('radio_items_all_or_month', 'value')],
                  [State('time_picker', 'value'),
                   State('my_date_picker', 'start_date'),
                   State('my_date_picker', 'end_date'),
                   State('upload_dataset', 'contents')]
                  )
    def update_graph_first_to_send_message(n_clicks_1, n_clicks_2, all_or_month: str, time_limit: time,
                                           start_date: datetime, end_date: datetime, contents) -> go.Figure:
        if contents is not None:
            df_new: pd.DataFrame = df.loc[(df['datetime'] <= end_date) & (df['datetime'] >= start_date), :]
            if type(time_limit) == str:
                time_limit = datetime.strptime(time_limit, "%H:%M").time()
            return first_to_send_message(df_new, list_names, time_limit, all_or_month)
        else:
            return dash.no_update

    @app.callback(Output('graph_number_of_specific_word', 'figure'),
                  [Input('submit_button_utilisation_of_a_specific_word', 'n_clicks'),
                   Input('submit_button', 'n_clicks'),
                   Input('radio_items_day_month_all', 'value')],
                  [State('word_picker', 'value'),
                   State('my_date_picker', 'start_date'),
                   State('my_date_picker', 'end_date'),
                   State('upload_dataset', 'contents')]
                  )
    def update_graph_number_of_specific_word(n_clicks_1, n_clicks_2, all_or_month_or_day: str, symbol: str,
                                             start_date: datetime, end_date: datetime, contents) -> go.Figure:
        if contents is not None:
            df_new: pd.DataFrame = df.loc[(df['datetime'] <= end_date) & (df['datetime'] >= start_date), :]
            return find_number_of(df, symbol, list_names, all_or_month_or_day)
        else:
            return dash.no_update

    @app.callback(Output('show_number_of_stickers', 'children'),
                  Input('slider_number_stickers', 'value'))
    def update_show_number_of_stickers(number_input: int) -> str:
        return "Choose the number of stickers you want to show :  {}".format(str(number_input))

    @app.callback(Output('graph_show_stickers', 'figure'),
                  [Input('submit_button', 'n_clicks'),
                   Input('radio_items_all_or_month_stickers', 'value'),
                   Input("slider_number_stickers", "value")],
                  [State('my_date_picker', 'start_date'),
                   State('my_date_picker', 'end_date'),
                   State('upload_dataset', 'contents')]
                  )
    def update_graph_show_stickers(n_clicks, all_or_month: str, top_number: int, start_date: datetime,
                                   end_date: datetime, contents) -> go.Figure:
        if contents is not None:
            df_new: pd.DataFrame = df.loc[(df['datetime'] <= end_date) & (df['datetime'] >= start_date), :]
            return find_top_stickers_used_dash(df_new, top_number, all_or_month, list_names)[0]
        else:
            return dash.no_update

    @app.callback(Output('img_stickers', 'children'),
                  [Input('graph_show_stickers', 'clickData'),
                   Input('submit_button', 'n_clicks'),
                   Input('radio_items_all_or_month_stickers', 'value'),
                   Input("slider_number_stickers", "value"),
                   Input('upload_stickers', 'contents')],
                  [State('my_date_picker', 'start_date'),
                   State('my_date_picker', 'end_date'),
                   State('upload_stickers', 'filename'),
                   State('upload_dataset', 'contents')]
                  )
    def update_img_stickers(clickData, n_clicks, all_or_month: str, top_number: int, list_of_contents,
                            start_date: datetime,
                            end_date: datetime, list_of_names: List[str], contents):
        if contents is not None:
            list_path = find_top_stickers_used_dash(df, top_number, all_or_month, list_names)[1]
            if all_or_month == 'all':
                if clickData:
                    name = clickData['points'][0]['x']
                    count = clickData['points'][0]['y']
                    img_encoded = list_path[name]['path']
                    images_div = []
                    for image in img_encoded:
                        for index, filename in enumerate(list_of_names):
                            if (str("stickers/") + str(filename)) == image:
                                images_div.append(generate_image(list_of_contents[index], style={'height': '20%',
                                                                                                 'width': '20%',
                                                                                                 'float': 'left',
                                                                                                 'position': 'relative',
                                                                                                 'padding-top': 0,
                                                                                                 'padding-right': 5
                                                                                                 }))
                    return html.Div(images_div)
            elif all_or_month == 'month':
                if clickData:
                    name = list(list_path.keys())[clickData['points'][0]['curveNumber']]
                    count = clickData['points'][0]['y']
                    year_month = clickData['points'][0]['x']
                    img_encoded = list_path[name].loc[(list_path[name]['file'] == count) & (
                            list_path[name]['year_month'] == str(year_month)), 'path'].values[0]
                    images_div = []
                    for image in img_encoded:
                        for index, filename in enumerate(list_of_names):
                            if (str("stickers/") + str(filename)) == image:
                                images_div.append(generate_image(list_of_contents[index], style={'height': '20%',
                                                                                                 'width': '20%',
                                                                                                 'float': 'left',
                                                                                                 'position': 'relative',
                                                                                                 'padding-top': 0,
                                                                                                 'padding-right': 5
                                                                                                 }))
                    return html.Div(images_div)
        else:
            return dash.no_update

    @app.callback(Output('nlp_radio_items_all_or_month_or_weekday', 'options'),
                  [Input('dropdown_name_nlp', 'value')]
                  )
    def disabled_radio_button_when_comparison(name_choose: str):
        if name_choose == "comparison":
            return [{"label": "All", "value": "all"},
                    {"label": "By month", "value": "month", "disabled": True},
                    {"label": "Weekday", "value": "weekday", "disabled": True}
                    ]

        else:
            return [{"label": "All", "value": "all"},
                    {"label": "By month", "value": "month"},
                    {"label": "Weekday", "value": "weekday"}
                    ]

    @app.callback(Output('data_prep_nlp_empty_div', 'children'),
                  [Input('data_prep_nlp_button', 'n_clicks')]
                  )
    def update_spinner_data_prep_nlp(n_clicks):
        if n_clicks > 0:
            global df_nlp
            df_nlp = data_prep_nlp(df)
            return 0

    @app.callback(Output('dropdown_name_nlp', 'options'),
                  Input('data_prep_nlp_button', 'n_clicks')
                  )
    def update_list_names_dropdown_nlp(n_clicks: int):
        if n_clicks > 0:
            if 'df' in globals():
                list_names = df['from'].unique()
                return [{"label": name, "value": name} for name in list_names] + [{"label": "Everyone", "value": "all"},
                                                                          {"label": "Comparison",
                                                                           "value": 'comparison'}]

        else:
            return dash.no_update

    @app.callback(Output('graph_nlp', 'figure'),
                  [Input('dropdown_name_nlp', 'value'),
                   Input('nlp_radio_items_all_or_month_or_weekday', 'value')
                   ]
                  )
    def update_graph_nlp(name_choose: str, all_or_month_or_weekday: str):
        if 'df_nlp' in globals():
            return graph_analyse_sentiments(df_nlp, all_or_month_or_weekday, name_choose, list_names)
        else:
            return dash.no_update

    @app.callback(Output('show_number_of_words_wordcloud', 'children'),
                  Input('slider_number_words_wordcloud', 'value')
                  )
    def update_show_number_of_stickers(number_input: int) -> str:
        return "Choose the number of words you want to show :  {}".format(str(number_input))

    @app.callback(Output('img_wordcloud', 'children'),
                  [Input('slider_number_words_wordcloud', 'value'),
                   Input('data_prep_nlp_button', 'n_clicks')]
                  )
    def update_wordcloud(number_words: int, n_clicks: int):
        if 'df_nlp' in globals():
            if n_clicks > 0:
                img = BytesIO()
                wordcloud_most_used_word(df_nlp, number_words).save(img, format='PNG')
                return generate_image('data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode()),
                                      style={
                                          'height': '100%',
                                          'width': '100%',
                                          'position': 'relative',
                                          'float': 'center',
                                          'padding-top': 30,
                                          'padding-right': 30,
                                          'padding-bot': 30,
                                          'padding-left': 30
                                      }
                                      )
        else:
            return dash.no_update

    return app

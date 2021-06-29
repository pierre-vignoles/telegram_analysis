from typing import List

import pandas as pd
import base64
import io
import json
import os
from datetime import datetime
from emoji import UNICODE_EMOJI


def text_has_emoji(text):
    for character in text:
        if character in UNICODE_EMOJI['en']:
            return 1
    return 0


def upload_json(contents, filename) -> pd.DataFrame:
    df: pd.Dataframe = pd.DataFrame()
    if contents is not None:
        content_type, content_string = contents[0].split(',')
        decoded = base64.b64decode(content_string + '==')
        if 'json' in filename[0]:
            data = json.load(io.BytesIO(decoded))
            df = df.append(data[u'messages'])
        elif 'csv' in filename[0]:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename[0]:
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            print("Not a valid file")

        ## Data Prep
        # Delete first message : 'joined telegram'
        if 'action' in df.columns:
            if df.loc[0, 'action'] == 'joined_telegram':
                df = df.drop(df.index[0])

        # Fill all na values
        df = df.fillna(0)

        # Merge column photo with media_type
        if 'photo' in df.columns:
            df['media_type'] = df.apply(lambda x: 'photo' if x['photo'] != 0 else x['media_type'], axis=1)

        # Replace lines with link by NanValues in the column 'text' and merge column text with media type (link)
        df['media_type'] = df.apply(lambda x: 'link' if type(x['text']) == list else x['media_type'], axis=1)
        df['text'] = df.apply(lambda x: '' if type(x['text']) == list else x['text'], axis=1)

        # df = df.loc[df['text'].apply(type) != list]

        # Merge column action(phone_call) with media_type and actor with from
        if ('discard_reason' in df.columns) & ('action' in df.columns):
            df['media_type'] = df.apply(lambda x: 'phone_call' if (
                    (x['action'] == 'phone_call') & (x['discard_reason'] in ('hangup', 'disconnect')) & (
                    x['duration_seconds'] >= 100)) else x['media_type'], axis=1)
        elif 'action' in df.columns:
            df['media_type'] = df.apply(
                lambda x: 'phone_call' if ((x['action'] == 'phone_call') & (x['duration_seconds'] >= 100)) else x[
                    'media_type'], axis=1)

        df['from'] = df.apply(lambda x: x['actor'] if x['from'] == 0 else x['from'], axis=1)

        # Get dummies of media_type
        df = pd.get_dummies(df, columns=['media_type'])
        df = df.drop(columns=['media_type_0'])

        # Column emoji
        df['media_type_emoji'] = df['text'].apply(lambda x: text_has_emoji(x))

        # Replace '' in the column 'text' with 'NaNValue'
        df['text'] = df['text'].apply(lambda x: 'NaNValue' if x == '' else x)

        # Rename column date into datetime
        df.rename(columns={'date': 'datetime'}, inplace=True)

        # Convert date string into date format
        df['datetime'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))

        # Delete line if from = 0
        df = df[df['from'] != 0]

        # Take only the first part of the name
        df['from'] = df['from'].apply(lambda x: x.split(" ")[0])

        # Add the weekday
        df['weekday'] = df['datetime'].apply(lambda x: x.weekday())
        # Transformation of the weekday from numbers to words
        list_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df['weekday'] = df['weekday'].apply(lambda x: list_day[x])

        # Reset index
        df = df.reset_index()

        # keep only some useful columns
        list_columns: List[str] = ['id', 'datetime', 'text', 'from', 'file', 'media_type_animation',
                                   'media_type_audio_file', 'media_type_phone_call', 'duration_seconds',
                                   'media_type_photo',
                                   'media_type_sticker', 'media_type_video_file', 'media_type_voice_message',
                                   'media_type_link', 'media_type_emoji', 'weekday']
        list_final_columns: List[str] = []
        for column in list_columns:
            if column in df.columns:
                list_final_columns.append(column)
        df = df[list_final_columns]

        return df

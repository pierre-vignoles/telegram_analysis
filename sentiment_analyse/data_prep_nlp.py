import re
from typing import List

import spacy
import pandas as pd
from emoji import UNICODE_EMOJI
from pathlib import Path

from textblob import TextBlob, Blobber
from textblob_fr import PatternTagger, PatternAnalyzer


# from nltk.stem.snowball import SnowballStemmer


def init_nlp():
    # load Spacy french
    global nlp, stopWords
    nlp = spacy.load("fr_core_news_sm")
    # load stop words and add some
    stopWords = nlp.Defaults.stop_words
    stop_words_add = ['t', 'c', 'j', 'p', 'pr', 'l', 'd', ' ', 'm']
    for el in stop_words_add:
        nlp.Defaults.stop_words.add(el)
    return nlp, stopWords


def nlp_pipeline(text: str) -> str:
    text = text.lower()
    text = text.replace('\n', ' ').replace('\r', '')
    text = ' '.join(text.split())
    text = re.sub(r"[A-Za-z\.]*[0-9]+[A-Za-z%°\.]*", "", text)
    text = re.sub(r"(\s\-\s|-$)", "", text)
    text = re.sub(r"[,\!\?\%\(\)\/\"]", "", text)
    text = re.sub(r"\&\S*\s", "", text)
    text = re.sub(r"\&", "", text)
    text = re.sub(r"\+", "", text)
    text = re.sub(r"\#", "", text)
    text = re.sub(r"\$", "", text)
    text = re.sub(r"\£", "", text)
    text = re.sub(r"\%", "", text)
    text = re.sub(r"\:", "", text)
    text = re.sub(r"\@", "", text)
    text = re.sub(r"\-", "", text)
    return text


def init_blobber() -> Blobber():
    tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
    return tb


# def init_stemmer() -> SnowballStemmer:
#     stemmer = SnowballStemmer(language='french')
#     return stemmer


# Split by words
def return_token(sentence: str, nlp) -> List[str]:
    # Tokeniser la phrase
    doc = nlp(sentence)
    # Retourner le texte de chaque token
    return [X.text for X in doc]


def return_split_words(sentence: str) -> List[str]:
    sentence = sentence.lower()
    return re.sub("\W", " ", sentence).split()


# Delete emoji
def text_has_emoji(text):
    for character in text:
        if character in UNICODE_EMOJI['en']:
            return True
    return False


def delete_emoji(list_words: List[str]) -> List[str]:
    no_emoji: List[str] = []
    for word in list_words:
        if not text_has_emoji(word):
            no_emoji.append(word)
    return no_emoji


# Stop words
def return_clean_words(list_words: List[str], stopWords) -> List[str]:
    clean_words: List[str] = []
    for word in list_words:
        if word not in stopWords:
            clean_words.append(word)
    return clean_words


# def return_stem(list_words: list, stemmer: SnowballStemmer) -> List[str]:
#     stem_words: list = []
#     for word in list_words:
#         stem_words.append(stemmer.stem(word))
#     return stem_words


# Main
def data_prep_nlp(df: pd.DataFrame()) -> pd.DataFrame:
    # Init nlp and stop words
    nlp, stopWords = init_nlp()
    df_copy: pd.DataFrame = df.copy()

    # Delete NaNValue
    df_copy = df_copy.loc[df_copy['text'] != 'NaNValue']

    # nlp_pipeline
    df_copy['text'] = df_copy['text'].apply(lambda x: nlp_pipeline(x))

    # return_token
    df_copy['text_prep_split_words'] = df_copy['text'].apply(lambda x: return_split_words(x))

    # Delete emoji
    df_copy['text_prep_no_emoji'] = df_copy['text_prep_split_words'].apply(lambda x: delete_emoji(x))

    # Stop words
    df_copy['text_prep_clean_words'] = df_copy['text_prep_no_emoji'].apply(
        lambda x: return_clean_words(x, stopWords))
    df_copy = df_copy.drop(["text_prep_no_emoji"], axis=1)

    # # Stemming
    # stemmer = init_stemmer()
    # df_copy['text_prep_stem_words'] = df_copy['text_prep_clean_words'].apply(lambda x: return_stem(x, stemmer))

    # Delete "[]" in text_prep_clean_words
    df_copy = df_copy.loc[df_copy['text_prep_clean_words'].map(len) > 0]

    # Delete columns
    df_copy = df_copy.reset_index()
    list_columns_to_drop = ["index", 'id', "file", "media_type_animation", "media_type_audio_file",
                            "media_type_phone_call", "media_type_photo", "media_type_sticker",
                            "media_type_video_file", "media_type_voice_message", "media_type_link",
                            "media_type_emoji"]
    for column in list_columns_to_drop:
        if column in df_copy.columns:
            df_copy = df_copy.drop([column], axis=1)

    # Month and year
    df_copy["month"] = df_copy["datetime"].apply(lambda x: x.month)
    df_copy["year"] = df_copy["datetime"].apply(lambda x: x.year)

    ## Sentiments analyse
    # init blobber
    tb: Blobber() = init_blobber()
    senti_list: List[str] = []
    for i in df_copy["text_prep_clean_words"]:
        i = ' '.join(i)
        vs = tb(i).sentiment[0]
        if vs > 0:
            senti_list.append('Positive')
        elif vs < 0:
            senti_list.append('Negative')
        else:
            senti_list.append('Neutral')
    df_copy["sentiment"] = senti_list

    return df_copy

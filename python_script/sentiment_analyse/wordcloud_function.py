from wordcloud import WordCloud
import pandas as pd


def wordcloud_most_used_word(df: pd.DataFrame, number_words: int):
    df = df.explode('text_prep_clean_words')
    df_top_used_word = dict(
        df.loc[df['text_prep_clean_words'].notnull(), 'text_prep_clean_words'].value_counts()[0:int(number_words)])

    wordcloud: WordCloud = WordCloud(background_color="#32383e",
                                     width=600,
                                     height=450)

    return wordcloud.generate_from_frequencies(frequencies=df_top_used_word).to_image()

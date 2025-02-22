import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
import emoji
import os
import re

extractor = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    num_messages = df.shape[0]
    words = [word for message in df["message"] for word in message.split()]
    num_media_messages = df[df["message"] == "Media Message"].shape[0]
    links = [url for message in df["message"] for url in extractor.find_urls(message)]
    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    user_counts = df["user"].value_counts().head()
    percentage_df = (df['user'].value_counts(normalize=True) * 100).reset_index().rename(
        columns={'index': 'name', 'user': 'Percentage'}
    )
    return user_counts, percentage_df

def create_wordcloud(selected_user, df):
    # Filter data for the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Check if there's any data to process
    if df.empty:
        print("No valid messages to process.")
        return None

    # Generate word frequencies from the message data
    word_freq = df['message'].value_counts().to_dict()

    # Create a WordCloud object
    wc = WordCloud(width=800, height=800, max_words=100, background_color='white')

    # Check for a proper font to handle emojis and special characters
    try:
        df_wc = wc.generate_from_frequencies(word_freq)
    except AttributeError as e:
        if 'textsize' in str(e):
            # Handle the 'textsize' issue using a fallback approach
            def patched_textsize(self, text, font=None, *args, **kwargs):
                return ImageDraw.ImageDraw.textbbox(self, (0, 0), text, font=font)[2:]

            ImageDraw.ImageDraw.textsize = patched_textsize
            df_wc = wc.generate_from_frequencies(word_freq)

    return df_wc
    
def most_common_words(selected_user, df):
    stop_words_path = os.path.join(os.getcwd(), 'stop_words.txt')
    try:
        with open(stop_words_path, 'r', encoding='utf-8') as f:
            stop_words = f.read()
    except FileNotFoundError:
        stop_words = []

    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != "Media Message"]

    words = [word for message in temp['message'] for word in message.lower().split() if word not in stop_words]
    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=["Word", "Count"])
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    emoji_list = [c for message in df['message'] for c in message if c in emoji.EMOJI_DATA]
    emoji_df = pd.DataFrame(Counter(emoji_list).most_common(), columns=['Emoji', 'Count'])
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return heatmap

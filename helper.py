import pandas as pd
from pyexpat.errors import messages
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
import re
extractor = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user !="overall":
        df = df[df["user"]==selected_user]
    #fetch the no. of messages
    num_messages = df.shape[0]

    #fetch the no. of words
    words=[]
    for message in df["message"]:
        words.extend(message.split())

    #fetch the no. of media message
    num_media_messages = df[df["message"]=="Media Message"].shape[0]

    #fetch the no. of link shared
    links = []
    for message in df["message"]:
        links.extend(extractor.find_urls(message))
    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x =df["user"].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
        columns ={'index':'name','user':'Percentage'})
    return x,df
def is_emoji(s):
    return s in emoji.EMOJI_DATA

def create_wordcloud(selected_user, df):
    with open('.venv/Scripts/stop_words.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read().splitlines()

    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != "Media Message"]

    def remove_stop_words_and_emojis(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words and not re.search(r'[^\w\s,]', word):
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="#d3d3d3")
    temp['message'] = temp['message'].apply(remove_stop_words_and_emojis)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc



def most_common_words(selected_user, df):
    with open('.venv/Scripts/stop_words.txt', 'r', encoding='utf-8') as f:  # Open with utf-8 encoding
        stop_words = f.read()

    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != "Media Message"]

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    # Get the most common words and create the dataframe with proper column names
    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=["Word", "Count"])
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    emoji_list = []
    for message in df['message']:
        emoji_list.extend([c for c in message if c in emoji.EMOJI_DATA])

    # Create a DataFrame with the most common emojis
    emoji_df = pd.DataFrame(Counter(emoji_list).most_common(len(Counter(emoji_list))))
    emoji_df.columns = ['Emoji', 'Count']  # Set proper column names
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    daily_timeline = df.groupby(df['only_date']).count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    heatmap= df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return heatmap
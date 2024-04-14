from urlextract import URLExtract
extract = URLExtract()
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import pandas as pd
from collections import Counter
import emoji
import seaborn as sns

def fetch_stats(selected_user,df):


    if selected_user != 'Overall Users':

        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]
    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    #     fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []

    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages, len(words), num_media_messages, len(links)

def most_buys_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index(). rename(columns = {'index': 'name', 'user': 'percent'})
    return x, df

def create_wordCloud(selected_user, df):

    if selected_user != 'Overall Users':
        df = df[df['user'] == selected_user]
    # df['message'] = df['message'].apply(lambda x: re.sub('[^a-zA-Z0-9 \n.]', '', x))

    wc = WordCloud(width= 600, height= 600, min_font_size= 10, background_color= 'white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df ):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall Users':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(15))
    return most_common_df

def emojis_finder(selected_user, df):
    if selected_user != 'Overall Users':
        df = df[df['user'] == selected_user]

    emojis_list = []
    for message in df['message']:
        emojis_list.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis_list).most_common(len(Counter(emojis_list))))
    return emoji_df


def monthly_time_line(selected_user, df):
    if selected_user != 'Overall Users':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(str(timeline['month_num'][i]) + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall Users':
        df = df[df['user'] == selected_user]

    daily_timeline= df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall Users':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def monthly_activity_map(selected_user, df):
    if selected_user != 'Overall Users':
        df = df[df['user'] == selected_user]

    return df['month_num'].value_counts()

def activity_heatmap(selected_user, df):

    if selected_user != 'Overall Users':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


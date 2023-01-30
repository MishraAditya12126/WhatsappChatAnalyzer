from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
extractor = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0] # total number of messages
    words = []
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    return num_messages, len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head().reset_index()
    x.rename(columns={'user':'no.of_messages'},inplace=True)
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    temp = df[df['user'] != 'group-notification']
    temp_df = temp[temp['message'] != '<Media omitted>']

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    f.close()
    def remove_stop_wordz(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp_df['message'] = temp_df['message'].apply(remove_stop_wordz)
    df_wc = wc.generate(temp_df['message'].str.cat(sep=" "))

    return df_wc

def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group-notification']
    temp_df = temp[temp['message'] != '<Media omitted>']

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    f.close()
    words = []

    for message in temp_df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))

def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def activity_month_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    td = df.groupby(['year', 'month_num', 'month_name'])['message'].count().reset_index()
    time = []
    for i in range(td.shape[0]):
        time.append(str(td['year'][i]) + '-' + td['month_name'][i])

    td['timeline'] = time

    td = td[['timeline', 'message']]
    td.rename(columns={'message':'msg_count'},inplace=True)

    return td

def activity_daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    td = df.groupby('only_date')['message'].count().reset_index()
    td.rename(columns={'only_date':'date','message':'msg_count'},inplace=True)

    return td

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df =df[df['user'] == selected_user]

    td = df['day_name'].value_counts().reset_index()
    td.rename(columns={'index':'day name','day_name':'msg_count'},inplace=True)
    return td

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df =df[df['user'] == selected_user]

    td = df['month_name'].value_counts().reset_index()
    td.rename(columns={'index':'month name','month_name':'msg_count'},inplace=True)
    return td

def user_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    pt = df.pivot_table(index='day_name',columns='hour',values='message',aggfunc='count').fillna(0)

    return pt
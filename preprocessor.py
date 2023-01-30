import re
import pandas as pd
def preprocess(data):
    pattern = '\d{2}\/\d{2}\/\d{2},\s\d{1,2}:\d{2}\s\w{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    # messages
    dates = re.findall(pattern, data)
    # dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # try:
    #     df['message_date'] = df['message_date'].str.replace('pm', 'PM')
    #     df['message_date'] = df['message_date'].str.replace('am', 'AM')
    # except:
    #     pass
    df['message_date'] = df['message_date'].str.split('-').str.get(0).str.strip()
    # convert message_date type
    def repl(x):
        if 'pm' in x:
            pattern = ',\s(\d{1,2})'
            hr = re.findall(pattern, x)
            if int(hr[0]) < 12:
                y = re.sub(',\s(?:\d{1,2})', ", " + str(int(hr[0]) + 12), x)
                return y
            else:
                return x
        else:
            pattern = ',\s(\d{1,2})'
            hr = re.findall(pattern, x)
            if int(hr[0]) == 12:
                y = re.sub(',\s(?:\d{1,2})', ", " + str(int(hr[0]) - 12), x)
                return y
            else:
                return x

    df['message_date'] = df['message_date'].apply(repl)
    df['message_date'] = df['message_date'].str.replace('pm', '').str.strip()
    df['message_date'] = df['message_date'].str.replace('am', '').str.strip()

    # # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('(\+\d{2}\s\d{5}\s\d{5})|(\w+):', message)
        try:
            entry.remove(None)
        except:
            pass
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group-notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_name'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['message'] = df['message'].str.replace(':', '').str.strip()
    return df
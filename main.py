import re
import pandas as pd

file= open('WhatsApp Chat with Sam 😁🥴.txt','r',encoding= 'utf-8')
data= file.read()
# print(data)

pattern= "\d{2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s"
messages= re.split(pattern, data)[1:]
# print(messages)


dates_pattern = "\d{2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m"
dates = re.findall(dates_pattern, data)
# print(dates)


df = pd.DataFrame({'user_messages': messages, 'messages_date':dates})
df['messages_date'] = df['messages_date'].str.strip()
df['messages_date'] = pd.to_datetime(df['messages_date'], format='%d/%m/%y, %I:%M %p')
df.rename(columns={'messages_date': 'date'}, inplace = True)
# print(df.head())
# print(df.shape)



# separate user & user_meassages
users  = []
messages = []
for message in df['user_messages']:
    entry = re.split('([\w\W]+?):\s',message)
    if entry[1:]:
        users.append(entry[1])
        messages.append(entry[2])
    else:
        users.append('notification')
        messages.append(entry[0])

df['user'] = users
df['message'] = messages
df.drop(columns=['user_messages'], inplace= True)

# print(df.head())

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['month_num'] = df['date'].dt.month_name()
df['only_date'] = df['date'].dt.date
df['day'] = df['date'].dt.day
df['date_name'] = df['date'].dt.day_name()
df['hour'] = df['date'].dt.hour
df['minute'] = df['date'].dt.minute

print(df.head())
print(df)
print(df.columns)
print(df.dtypes)
print(df.isnull().sum())
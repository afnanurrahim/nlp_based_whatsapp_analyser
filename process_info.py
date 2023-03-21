import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
import numpy as np

#1 get the info about total- msgs, words, media and links shared
def msgs_info(df):
    media=len(df[df["Message"]=="<Media omitted> "])
    df=df[df["Message"]!="<Media omitted> "]
    msgs=len(df)
    words=df['word_count'].sum()
    link_count=0
    for l in df['url']:
        link_count+=len(l)
    
    return df,{'msgs':msgs, 'words':words, 'media':media, 'links':link_count}

#2 
def monthly_msgs(df):
    month=df.groupby(['Month','Year'],as_index=False)
    month_df=pd.DataFrame()
    month_df=month['Message'].count()
    month_df['Month_year']=month_df['Month']+month_df['Year'].apply(str)
    fig = go.Figure(
    data=[go.Bar(x=month_df['Month_year'], y=month_df['Message'],marker_color='green')],
    layout=go.Layout(
        title=go.layout.Title(text="Monthly messages timeline")
        )
    )
    return fig

#3 
def daily_msgs(df):
    daily_df=df.groupby('Date',as_index=False)
    daily_df=daily_df['Message'].count()
    fig = go.Figure(
    data=[go.Scatter(x=daily_df['Date'], y=daily_df['Message'])],
    layout=go.Layout(
        title=go.layout.Title(text="Daily messages")
        )
    )
    return fig

#4 
def most_busy_weekday(df):
    weekday_df=df.groupby('Weekday',as_index=False)
    weekday_df=weekday_df['Message'].count()
    fig = go.Figure(
    data=[go.Bar(x=weekday_df['Weekday'], y=weekday_df['Message'],marker_color='red')],
    layout=go.Layout(
        title=go.layout.Title(text="Most busy weekday")
        )
    )
    fig.update_layout(width=350)
    return fig
#5
def most_busy_month(df):
    weekday_df=df.groupby('Month',as_index=False)
    weekday_df=weekday_df['Message'].count()
    fig = go.Figure(
    data=[go.Bar(x=weekday_df['Month'], y=weekday_df['Message'],marker_color='gold')],
    layout=go.Layout(
        title=go.layout.Title(text="Most busy month")
        )
    )
    fig.update_layout(width=350)
    return fig

#6
def polarity_msgs(df):
    positive=len(df[df['Polarity']>0])
    negative=len(df[df['Polarity']<0])
    neutral=len(df)-(positive+negative)
    count={'positive':positive,'negative':negative,'neutral':neutral}


    fig= go.Figure(
        data=[go.Pie(labels=['positive','negative','neutral'], values=[positive,negative,neutral])]
    )
    return count,fig

#7
def weekday_heatmap(df):
    weekday_df=df.groupby('Weekday')
    users_weekday_df=pd.DataFrame(columns=list(weekday_df.groups))
    for x in list(weekday_df.groups):
        weekday_info=weekday_df.get_group(x)
        msg_hr_count=weekday_info.groupby('Hour')['Message'].count()
        users_weekday_df[x]=msg_hr_count
    users_weekday_df=users_weekday_df.replace(np.nan,0)
    users_weekday_df=users_weekday_df.astype(int)
    users_weekday_df=users_weekday_df.reset_index()

    for t in range(0,24):                                   # add hours where no msgs were sent
        if t not in users_weekday_df['Hour'].values:
            users_weekday_df.loc[len(users_weekday_df)] = 0
            users_weekday_df.at[len(users_weekday_df)-1,'Hour']=t

    users_weekday_df=users_weekday_df.sort_values(by=['Hour'])
    users_weekday_df=users_weekday_df.set_index('Hour')
    fig = sns.heatmap(users_weekday_df, cmap="YlGnBu")

    return fig

#8 
def most_and_least_busy_users(df):
    senders_df=df.groupby('Sender')
    busy_users=senders_df['Message'].count()

    busy_users_table=pd.DataFrame({
        'user': busy_users.index.to_list(),
        'count': busy_users.values.tolist()
    })

    return busy_users_table

#9
def users_polarity(df):
    senders_df=df.groupby('Sender')
    users_polarity_df=pd.DataFrame(columns=['sender','positive','negative','neutral'])

    for s in senders_df['Polarity']:
        p=0;n=0;z=0
        for x in s[1]:
            if x>0:
                p+=1
            elif x<0:
                n+=1
            else:
                z+=1
        
        users_polarity_df.loc[len(users_polarity_df.index)] = [s[0], p, n, z] 
    
    return users_polarity_df

def combine_least_interactive_users(df, polarity):  # polarity = 'positive' / 'negative'
    user_df=df.sort_values(by=polarity,ascending=False)[['sender',polarity]]
    # Combine small percentages to 'Other'
    threshold = 2 
    small_percentages = user_df[user_df[polarity] / user_df[polarity].sum() < threshold/100]
    other_value = small_percentages[polarity].sum()
    user_df = user_df[user_df[polarity] / user_df[polarity].sum() >= threshold/100]
    user_df.loc[len(user_df)] = ['Others', other_value]

    return user_df
import streamlit as st
import get_dataframe
import process_info
import chatgpt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from wordcloud import WordCloud,STOPWORDS
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter


st.sidebar.title("whatsapp")

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    content = bytes_data.decode("utf-8")
    info_df=get_dataframe.create_dataframe(content).df_table()

    user_list = info_df['Sender'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Select user ",user_list)

    if st.sidebar.button("Show Analysis"):
        if selected_user != 'Overall':
            df = info_df[info_df['Sender'] == selected_user]
        else:
            df = info_df

        df,msgs_info=process_info.msgs_info(df)         # {'msgs':msgs, 'words':words, 'media':media, 'links':link_count}
        st.header('About')
        about= chatgpt.about_summary(list(df['Message']))
        st.write(about)

        col1, col2, col3, col4 = st.columns(4)

    #1
        with col1:
            st.header("Messages")
            st.subheader(msgs_info['msgs'])

        with col2:
            st.header("Words")
            st.subheader(msgs_info['words'])
        
        with col3:
            st.header("Media")
            st.subheader(msgs_info['media'])
        
        with col4:
            st.header("Links")
            st.subheader(msgs_info['links'])

    #2
        st.plotly_chart(process_info.monthly_msgs(df))
    #3
        st.plotly_chart(process_info.daily_msgs(df))

        weekday_col, month_col= st.columns(2,gap="large")
    #4
        with weekday_col:
            st.plotly_chart(process_info.most_busy_weekday(df))
    #5
        with month_col:
            st.plotly_chart(process_info.most_busy_month(df))

    #6 
        st. pyplot(process_info.weekday_heatmap(df).figure)

        if selected_user == 'Overall':
    #7 
            busy_users_df=process_info.most_and_least_busy_users(df)
            most_col, least_col = st.columns(2,gap='large')

            with most_col:
                st.subheader('Most busy users')
                st.table(busy_users_df.sort_values(by='count',ascending=False).head())
            with least_col:
                st.subheader('Least busy users')
                st.table(busy_users_df.sort_values(by='count').head())

    #8
        st.subheader("Polarity of messages")
        count, fig= process_info.polarity_msgs(df)
        positive_col, negative_col, neutral_col = st.columns(3, gap='large')

        with positive_col:
            st.subheader('positive')
            st.subheader(count['positive'])

        with negative_col:
            st.subheader('negative')
            st.subheader(count['negative'])
            
        with neutral_col:
            st.subheader('neutral')
            st.subheader(count['neutral'])

        st.plotly_chart(fig)

        if selected_user == 'Overall':
    #9
            users_polarity_df=process_info.users_polarity(df)

            positive_user_df= process_info.combine_least_interactive_users(users_polarity_df, 'positive')
            negative_user_df= process_info.combine_least_interactive_users(users_polarity_df, 'negative')

            st.subheader('Most Positive users')
            p_table_col, p_pie_chart_col = st.columns(2,gap='large')

            with p_table_col:
                st.table(positive_user_df.head())
            
            with p_pie_chart_col:
                fig= go.Figure(
                    data=[go.Pie(labels=positive_user_df['sender'], values=positive_user_df['positive'])]
                )
                st.plotly_chart(fig)

            st.subheader('Most Negative users') 
            n_table_col, n_pie_chart_col = st.columns(2,gap='large')

            with n_table_col:
                st.table(negative_user_df.head())
            
            with n_pie_chart_col:
                fig= go.Figure(
                    data=[go.Pie(labels=negative_user_df['sender'], values=negative_user_df['negative'])]
                )
                st.plotly_chart(fig)

    # removing stopwords

        temp=df['Message']
        stopwords_removed_msg=" "
        stopwords_removed_msg=stopwords_removed_msg.join(temp.to_list())

        stop_words = set(stopwords.words('english'))

        word_tokens = word_tokenize(stopwords_removed_msg)
        filtered_sentence = []

        for w in word_tokens:
            normal_string="".join(ch for ch in w if ch.isalnum())
            if (normal_string.lower() not in stop_words) and len(normal_string)>0 :
                filtered_sentence.append(normal_string)

        stopwords_removed_msg= " "
        stopwords_removed_msg=stopwords_removed_msg.join(filtered_sentence)

    #10
        st.subheader('Word Cloud')
        wc=WordCloud(background_color='white',
                stopwords=STOPWORDS)
        wc.generate(stopwords_removed_msg)
        st.image(wc.to_image(),width=700)

    #11
        split_it = stopwords_removed_msg.split()
        words_counter = Counter(split_it)
        most_occur = words_counter.most_common(10)
        most_occur=dict(most_occur)
        most_occur_df=pd.DataFrame({'Words': most_occur.keys(), 'Count': most_occur.values()})

        st.subheader('Most common words used')
        st.table(most_occur_df)

    #12
        emoji_list = [e for emoji in df['emoji'] for e in emoji]
        emoji_counter = Counter(emoji_list)
        most_occur_emoji = emoji_counter.most_common(10)
        most_occur_emoji=dict(most_occur_emoji)
        most_occur_emoji_df=pd.DataFrame({'Words': most_occur_emoji.keys(), 'Count': most_occur_emoji.values()})

        st.subheader('Most common emojis used')
        st.table(most_occur_emoji_df)



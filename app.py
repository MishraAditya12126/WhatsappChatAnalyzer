import streamlit as st
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title('Whatsapp chat Analyser')

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # fetch unique users

    user_list = df['user'].unique().tolist()
    user_list.remove('group-notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox('Show analysis wrt',user_list)

    # STATS area
    if st.sidebar.button('Show Analysis'):
            num_messages,num_words,num_media,num_links = helper.fetch_stats(selected_user,df)
            st.title(':offwhite[Top Statistics]')
            col1,col2,col3,col4 = st.columns(4)

            with col1:
                st.header(':orange[Total Messages]')
                st.title(num_messages)
            with col2:
                st.header(':green[Num of words]')
                st.title(num_words)
            with col3:
                st.header(':red[Num of media shared]')
                st.title(num_media)
            with col4:
                st.header(':blue[Num of links shared]')
                st.title(num_links)

            st.header(':green[Activity Timeline]')
            st.subheader(':blue[Monthly Activity timeline]')
            timeline = helper.activity_month_timeline(selected_user, df)
            fig = px.line(timeline, x='timeline', y='msg_count')
            st.plotly_chart(fig)

            st.subheader(':blue[Daily Activity timeline]')
            timeline = helper.activity_daily_timeline(selected_user, df)
            fig = px.line(timeline, x='date', y='msg_count')
            st.plotly_chart(fig)

            # finding the busiest users in the grp
            if selected_user == 'Overall':
                st.title(':red[Most Busy Users]')
                col1,col2 = st.columns(2)
                x,new_df = helper.most_busy_users(df)
                with col1:
                    st.subheader('Bar Chart for top users')
                    fig = px.bar(x,x = 'index',y = 'no.of_messages')
                    st.plotly_chart(fig)
                with col2:
                    st.subheader('Pie Chart for messages')
                    fig = px.pie(new_df,names='name',values='percent')
                    st.plotly_chart(fig)

            df_wc = helper.create_wordcloud(selected_user,df)
            st.title('Word Cloud')
            fig,ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            st.title(':blue[Most frequently used words]')
            most_common_df = helper.most_common_words(selected_user,df)
            fig = px.bar(most_common_df,x=1,y=0,orientation='h')
            st.plotly_chart(fig)

            emoji_df = helper.emoji_helper(selected_user,df)
            emoji_df.rename(columns={0:'emoji',1:'count'},inplace=True)
            st.title('Emoji Analysis')
            if emoji_df.shape[0] == 0:
                st.subheader(':green[No emojis sent by this person]')
            else:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(emoji_df)
                with col2:
                    fig = px.pie(emoji_df,names='emoji',values='count')
                    st.plotly_chart(fig)


            # activity map

            st.title('Activity Map')
            col1,col2 = st.columns(2)

            with col1:
                st.header('Most Busy Day')
                busy_day = helper.week_activity_map(selected_user,df)

                fig = px.bar(busy_day,x='day name',y='msg_count')
                st.plotly_chart(fig)

            with col2:
                st.header('Most Busy Month')
                busy_day = helper.month_activity_map(selected_user, df)

                fig = px.bar(busy_day, x='msg_count', y='month name',orientation='h')
                st.plotly_chart(fig)

            st.title(':orange[User Activity Heatmap] ')
            user_heatmap = helper.user_activity(selected_user,df)
            fig = px.imshow(user_heatmap)
            st.plotly_chart(fig)
import streamlit as st
import matplotlib.pyplot as plt
import Preprocessing,helper
import seaborn as sns
import os

st.sidebar.title("Whatsapp Chat Analyzer")
st.sidebar.write("Only upload the WhatsApp exported txt file.")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt"])

if uploaded_file is not None:
    # Check file extension
    file_extension = os.path.splitext(uploaded_file.name)[1]

    if file_extension != ".txt":
        st.sidebar.error("Please upload a valid WhatsApp exported .txt file.")
    else:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = Preprocessing.preprocess(data)

    user_list =  df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"overall")
    selected_user = st.sidebar.selectbox("show analysis with respect to ",user_list)
    if st.sidebar.button("show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Msgs")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links shared")
            st.title(num_links)
        #monthly_timeline
        st.title("Monthly Timeline chart")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        plt.plot(timeline['time'], timeline['message'],color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily_timeline
        st.title("Daily Timeline chart")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            plt.bar(busy_day.index,busy_day.values,color = 'darkblue')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            plt.bar(busy_month.index, busy_month.values, color='darkgreen')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        #activity heatmap
        heatmap = helper.activity_heatmap(selected_user, df)

        fig, ax = plt.subplots()
        sns.heatmap(heatmap, ax=ax, cmap='coolwarm',
                    cbar_kws={'label': 'Message Count'})  # You can customize the color map and color bar label
        ax.set_xlabel("Hour of the Day")
        ax.set_ylabel("Day of the Week")
        ax.set_title("Activity Heatmap")

        # Optionally, customize tick labels for better readability
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)  # Rotating labels for clarity
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

        st.pyplot(fig)

        #find the most busy user in group
        if selected_user=='overall':
            st.title("Most Busy Users")
            fig, ax = plt.subplots(figsize=(10,6))
            x,new_df= helper.most_busy_users(df)
            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color="red")
                fig.patch.set_facecolor('#d3d3d3')
                ax.set_xlabel('Users')
                ax.set_ylabel('Message Count')
                ax.set_title('Top Active Users')
                ax.tick_params(axis='x', rotation=45)
                st.pyplot(fig)
            st.title("WordCloud")
            with col2:
                st.dataframe(new_df)

        #WordCloud
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax =plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most Common Words
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        fig.patch.set_facecolor('#d3d3d3')
        ax.barh(most_common_df['Word'],most_common_df['Count'],color = "red")
        ax.set_xlabel('Words')
        ax.set_ylabel('Counts')
        ax.set_title('Most Common Words')
        st.title("Most Common Words")
        st.pyplot(fig)

        #emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            plt.rcParams['font.family'] = 'Segoe UI Emoji'
            # Ensure the 'Count' column contains numeric values for the pie chart
            ax.pie(emoji_df["Count"], labels=emoji_df["Emoji"], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig)
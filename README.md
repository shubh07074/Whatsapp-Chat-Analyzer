# Whatsapp-Chat-Analyzer
This project analyzes user activity from messaging data to provide insights such as most active users, word cloud, emoji usage, daily, weekly, and monthly activity trends. It uses Python libraries like pandas, seaborn, wordcloud, and Streamlit for visualizations and interactive reporting.

#WhatsApp Activity Analysis and Visualization
This project aims to analyze and visualize WhatsApp chat data to gain insights into user activity, message trends, and engagement. Using data from WhatsApp chat exports, the system processes and generates multiple visualizations to help users understand their messaging behavior, including message counts, word clouds, emoji usage, and activity heatmaps.

#Features:
Message Statistics: Provides key statistics such as the total number of messages, word count, number of media messages, and links shared in a selected chat or for all users.
Most Active Users: Identifies and displays the most active users in the chat, along with their message distribution as a percentage.
Word Cloud: Generates a word cloud that visualizes the most frequently used words in the chat, excluding stop words and emojis.
Emoji Analysis: Analyzes and displays the most commonly used emojis in the chat.
Monthly and Daily Timeline: Provides timelines showing the frequency of messages over time, including daily and monthly activity trends.
Weekly Activity Heatmap: A heatmap visualization that displays user activity patterns across the days of the week and hours of the day.
Data Preprocessing:
The project preprocesses WhatsApp chat data to remove group notifications, media messages, and stop words. It also handles the extraction and cleaning of URLs and emojis from the messages. The data is then aggregated to derive meaningful insights, such as activity timelines and the most common words and emojis.

#Visualization:
Using Matplotlib, Seaborn, and WordCloud, the project generates visualizations like bar charts, heatmaps, and word clouds. These visualizations are interactive and presented through a web application built using Streamlit.

#Libraries and Tools Used:
Pandas: Data manipulation and analysis
PyExpat: Parsing XML-based chat exports
URLExtract: Extracting URLs from messages
WordCloud: Generating word clouds
Seaborn & Matplotlib: Data visualization
Streamlit: Web app framework for displaying results interactively
Emoji: Emoji detection in text
How to Run:
Clone the repository.
Install required libraries:
pip install -r requirements.txt
Run the Streamlit app:
streamlit run app.py
This project provides a comprehensive analysis of WhatsApp chat data and is useful for anyone interested in tracking their messaging behavior or analyzing group chat dynamics.

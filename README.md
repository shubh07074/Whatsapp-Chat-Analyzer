
User Activity Analysis
This project analyzes user activity from messaging data, providing insights into user engagement, activity patterns, most common words, emoji usage, and more. The project leverages Python libraries like Pandas, Seaborn, WordCloud, and Streamlit to create interactive visualizations.

Features
User Stats: Displays the number of messages, words, media messages, and links shared by the selected user.
Most Active Users: Identifies and displays the most active users along with their message percentages.
Word Cloud: Generates a word cloud visualizing the most frequent words used, excluding stop words and emojis.
Emoji Analysis: Displays the most commonly used emojis by the user or the entire group.
Activity Timeline: Provides a timeline of user activity on a daily and monthly basis.
Weekly Activity Map: Shows a heatmap of activity across different days of the week.
Monthly Activity Map: Displays a heatmap of activity across different months.
Installation
To run this project, you need to have Python installed along with the required dependencies. Follow the steps below:

Clone the repository:
git clone https://github.com/your-username/user-activity-analysis.git
cd user-activity-analysis

Install the necessary dependencies:
pip install -r requirements.txt

Download or upload your messaging data (in txt format) to the project directory.

Run the app:
streamlit run app.py

Dependencies
pandas
seaborn
wordcloud
urlextract
emoji
matplotlib
streamlit

Usage
Upload your messaging data in txt format.
Select the user whose activity you want to analyze or choose "overall" for group-wide insights.
Explore the visualizations and insights, including user activity statistics, word clouds, emoji usage, and activity heatmaps.

Example Output
Activity Heatmap: Visualizes activity levels throughout the week or month.
Word Cloud: Displays the most used words by a selected user or group.
Emoji Analysis: Highlights the most frequently used emojis.

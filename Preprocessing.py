import re
import pandas as pd

def preprocess(data):
    # Define pattern for datetime
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    
    # Split messages and dates
    messages = re.split(pattern, data)[1:]  # Skipping the first empty entry
    dates = re.findall(pattern, data)

    # Create DataFrame with messages and corresponding dates
    df = pd.DataFrame({"user_message": messages, "message_date": dates})

    # Convert 'message_date' to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    df.rename(columns={'message_date': "date"}, inplace=True)
    
    # Initialize lists for users and messages
    users = []
    message_contents = []

    # Split each message into user and message text
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if len(entry) > 1:  # Check if there is a user identified
            users.append(entry[1])
            message_contents.append(entry[2])
        else:
            users.append('group_notification')
            message_contents.append(entry[0])

    # Assign users and messages to respective columns
    df['user'] = users
    df['message'] = message_contents
    
    # Drop the original 'user_message' column
    df.drop(columns=['user_message'], inplace=True)
    
    # Extract date parts (year, month, day, hour, minute, etc.)
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute
    
    # Replace '<Media omitted>' text with 'Media Message'
    df['message'] = df['message'].str.replace('<Media omitted>\n', 'Media Message', regex=True)

    # Determine periods (hour ranges)
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append("23-00")  # Special case for 23-00
        elif hour == 0:
            period.append("00-01")
        else:
            period.append(f"{hour}-{hour + 1}")

    # Add the period column
    df['period'] = period

    return df

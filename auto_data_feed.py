from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
import isodate
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('YT_API_KEY')
CHANNEL_ID = os.getenv('YT_CHANNEL_ID')

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to get subscriber count
def get_subscriber_count(youtube, channel_id):
    request = youtube.channels().list(
        part='statistics',
        id=channel_id
    )
    response = request.execute()
    subs = int(response['items'][0]['statistics']['subscriberCount'])
    return subs

# Function to get all video IDs and published dates
def get_all_videos(youtube, channel_id):
    videos = []
    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        maxResults=50,
        order="date",
        type="video"
    )
    response = request.execute()

    while request is not None:
        for item in response['items']:
            video_id = item['id']['videoId']
            published_at = item['snippet']['publishedAt']
            videos.append({'id': video_id, 'publishedAt': published_at})
        request = youtube.search().list_next(request, response)
        if request:
            response = request.execute()
        else:
            break
    return videos

# Function to classify videos into longs and shorts
def classify_videos(youtube, videos):
    longs = []
    shorts = []

    for video in videos:
        request = youtube.videos().list(
            part='contentDetails,statistics',
            id=video['id']
        )
        response = request.execute()
        item = response['items'][0]
        duration = isodate.parse_duration(item['contentDetails']['duration']).total_seconds()

        stats = item['statistics']
        views = int(stats.get('viewCount', 0))

        video_data = {
            'id': video['id'],
            'publishedAt': video['publishedAt'],
            'views': views
        }

        if duration > 150:
            longs.append(video_data)
        else:
            shorts.append(video_data)

    longs_sorted = sorted(longs, key=lambda x: x['publishedAt'])
    shorts_sorted = sorted(shorts, key=lambda x: x['publishedAt'])

    return longs_sorted, shorts_sorted

# MAIN PROCESS
today = datetime.now().strftime('%d.%m.%y')  # to match your date format
subs = get_subscriber_count(youtube, channel_id)
videos = get_all_videos(youtube, channel_id)
longs, shorts = classify_videos(youtube, videos)

# Build row
row = {'date': today, 'subs': subs}

# Add longs
for idx, vid in enumerate(longs):
    row[f'long{idx+1}'] = vid['views']

# Add shorts
for idx, vid in enumerate(shorts):
    row[f'short{idx+1}'] = vid['views']

# Load or create Excel
file_name = 'daily_data.xlsx'

if os.path.exists(file_name):
    df = pd.read_excel(file_name)
else:
    df = pd.DataFrame()

# Append new row
df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
df.to_excel(file_name, index=False)

print("✅ Data updated successfully for", today)
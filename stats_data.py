import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import os
import isodate
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('YT_API_KEY')
CHANNEL_ID = os.getenv('YT_CHANNEL_ID')

# File name
file_name = 'daily_data.xlsx'

# Today's date (format: dd.mm.yy)
today = datetime.now().strftime('%d.%m.%y')

# Load existing data or create new
if os.path.exists(file_name):
    df = pd.read_excel(file_name)
else:
    df = pd.DataFrame(columns=['date', 'subs'])

# Check if today's data already exists
if today not in df['date'].astype(str).values:
    # Get channel subscriber count
    channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={API_KEY}"
    channel_response = requests.get(channel_url).json()
    subs = int(channel_response['items'][0]['statistics']['subscriberCount'])

    # Get video list
    videos = []
    next_page = ''
    while True:
        search_url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=50&pageToken={next_page}"
        search_response = requests.get(search_url).json()

        for item in search_response['items']:
            if item['id']['kind'] == 'youtube#video':
                videos.append(item['id']['videoId'])

        if 'nextPageToken' in search_response:
            next_page = search_response['nextPageToken']
        else:
            break

    longs, shorts = {}, {}

    for video_id in videos:
        stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics&id={video_id}&key={API_KEY}"
        stats_response = requests.get(stats_url).json()

        if not stats_response['items']:
            continue

        item = stats_response['items'][0]
        views = int(item['statistics'].get('viewCount', 0))
        duration = item['contentDetails']['duration']
        duration_seconds = isodate.parse_duration(duration).total_seconds()

        if duration_seconds >= 150:
            longs[f'long_{video_id}'] = views
        else:
            shorts[f'short_{video_id}'] = views

    # Prepare today's data row
    today_data = {'date': today, 'subs': subs}
    today_data.update(longs)
    today_data.update(shorts)

    # Append today's data
    df = pd.concat([df, pd.DataFrame([today_data])], ignore_index=True)

    # Fill missing columns dynamically
    df = df.fillna(0)

    # Save updated data
    df.to_excel(file_name, index=False)

# ✅ Analytics section — runs always

# Reload full data (in case new row was added)
df = pd.read_excel(file_name)

# Date formatting
df['date'] = pd.to_datetime(df['date'], format='%d.%m.%y')
df = df.sort_values('date')

# Subs growth
df['subs_growth'] = df['subs'].diff().fillna(0)

# Detect long & short columns dynamically
long_cols = [col for col in df.columns if col.startswith('long')]
short_cols = [col for col in df.columns if col.startswith('short')]

# ✅ VERY IMPORTANT FIX — convert to numeric to avoid sum() errors
for col in long_cols + short_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

df['long_total'] = df[long_cols].sum(axis=1)
df['short_total'] = df[short_cols].sum(axis=1)
df['total_views'] = df['long_total'] + df['short_total']
df['views_growth'] = df['total_views'].diff().fillna(0)

# Save analytics report
df.to_excel('analytics_report.xlsx', index=False)

# Plot: Sub growth
plt.style.use('seaborn-v0_8-darkgrid')
plt.figure(figsize=(10,6))
plt.plot(df['date'], df['subs'], marker='o', label='Total Subs')
plt.title('Subscribers Growth Over Time')
plt.xlabel('Date')
plt.ylabel('Subscribers')
plt.legend()
plt.tight_layout()
plt.savefig('subs_growth.png')
plt.close()

# Plot: Longs & Shorts total views
plt.figure(figsize=(10,6))
plt.plot(df['date'], df['long_total'], marker='o', label='Longs Total Views')
plt.plot(df['date'], df['short_total'], marker='o', label='Shorts Total Views')
plt.title('Longs & Shorts Views Over Time')
plt.xlabel('Date')
plt.ylabel('Views')
plt.legend()
plt.tight_layout()
plt.savefig('total_views.png')
plt.close()

# Plot: Daily view growth
plt.figure(figsize=(10,6))
plt.bar(df['date'], df['views_growth'], color='skyblue')
plt.title('Daily New Views')
plt.xlabel('Date') 
plt.ylabel('Views Growth')
plt.tight_layout()
plt.savefig('daily_deltas.png')
plt.close()

# Top performing videos
latest_row = df.iloc[-1]
top_longs = latest_row[long_cols].sort_values(ascending=False)
top_shorts = latest_row[short_cols].sort_values(ascending=False)

# Export Top Videos to Excel (append to report)
with pd.ExcelWriter('analytics_report.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    top_longs.to_frame(name='Views').to_excel(writer, sheet_name='Top_Longs')
    top_shorts.to_frame(name='Views').to_excel(writer, sheet_name='Top_Shorts')

print("\n✅ Automation + Analytics fully completed.")

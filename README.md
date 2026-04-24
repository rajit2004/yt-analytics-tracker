# 📊 YouTube Analytics Tracker

> Automatically tracks daily YouTube channel stats — subscribers, views, Longs vs Shorts performance — and generates charts and Excel reports using the YouTube Data API v3.

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)](https://python.org)
[![YouTube API](https://img.shields.io/badge/YouTube-Data%20API%20v3-red?style=flat&logo=youtube)](https://developers.google.com/youtube/v3)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/rajit2004?style=flat&logo=githubsponsors&color=EA4AAA)](https://github.com/sponsors/rajit2004)

---

## 📸 Sample Output

<table>
  <tr>
    <td><strong>Subscribers Growth</strong><br/><img src="outputs/subs_growth.png" width="350"/></td>
    <td><strong>Longs vs Shorts Views</strong><br/><img src="outputs/total_views.png" width="350"/></td>
  </tr>
  <tr>
    <td><strong>Daily View Deltas</strong><br/><img src="outputs/daily_deltas.png" width="350"/></td>
    <td><strong>Analytics Report (Excel)</strong><br/>Generated in <code>outputs/analytics_report.xlsx</code></td>
  </tr>
</table>

---

## ✨ Features

- 📅 **Daily data logging** — tracks subscribers and video views every day
- 🎥 **Longs vs Shorts classification** — automatically separates videos by duration (>150s = Long)
- 📈 **3 auto-generated charts** — subs growth, views over time, daily view deltas
- 📄 **Excel analytics report** — full data + top performing videos by type
- 🔒 **Secure** — API key stored in `.env`, never committed to git

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core scripting |
| YouTube Data API v3 | Fetching channel & video stats |
| Pandas | Data processing & Excel I/O |
| Matplotlib | Chart generation |
| OpenPyXL | Excel report writing |
| python-dotenv | Secure API key management |

---

## ⚡ Setup & Usage

### 1. Clone the repo
```bash
git clone https://github.com/rajit2004/yt-analytics-tracker.git
cd yt-analytics-tracker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
```bash
cp .env.example .env
```
Then open `.env` and fill in your credentials:
```
YT_API_KEY=your_youtube_api_key_here
YT_CHANNEL_ID=your_channel_id_here
```

> 🔑 Get your API key from [Google Cloud Console](https://console.cloud.google.com/) → Enable YouTube Data API v3

### 4. Run the tracker
```bash
# Simple version (uses requests)
python stats_data.py

# Modular version (uses Google API client)
python auto_data_feed.py
```

---

## 📁 Project Structure

```
yt-analytics-tracker/
├── stats_data.py          # Main tracker script
├── auto_data_feed.py      # Modular API client version
├── .env                   # Your API key (never committed)
├── .env.example           # Template for setup
├── .gitignore
├── requirements.txt
└── outputs/               # Generated files
    ├── analytics_report.xlsx
    ├── subs_growth.png
    ├── total_views.png
    └── daily_deltas.png
```

---

## 🔄 Automate Daily Runs

To run this automatically every day, set up a cron job (Linux/Mac):
```bash
0 9 * * * cd /path/to/yt-analytics-tracker && python stats_data.py
```

Or use Windows Task Scheduler to run `stats_data.py` daily.

---

## 💖 Support

If this project helped you, consider supporting my work:

[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink?style=for-the-badge&logo=githubsponsors)](https://github.com/sponsors/rajit2004)

---

## 👨‍💻 Author

**Ranesh Rajit** — B.Tech CS Student, India

[![GitHub](https://img.shields.io/badge/GitHub-rajit2004-black?style=flat&logo=github)](https://github.com/rajit2004)

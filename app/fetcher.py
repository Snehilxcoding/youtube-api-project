import requests
import time
from db import videos_collection

API_KEY = "YOUR_API_KEY"


def fetch_videos(query):
    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "order": "date",
        "maxResults": 10,
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    for item in data.get("items", []):
        video_id = item["id"]["videoId"]

        video = {
            "title": item["snippet"]["title"],
            "video_id": video_id,
            "published_at": item["snippet"]["publishedAt"],
            "thumbnail": item["snippet"]["thumbnails"]["default"]["url"]
        }

        if not videos_collection.find_one({"video_id": video_id}):
            videos_collection.insert_one(video)


def run_fetcher():
    while True:
        print("Fetching latest videos...")
        fetch_videos("cricket")
        time.sleep(10)
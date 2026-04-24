import requests
import time
import logging
from app.config import API_KEYS, QUERIES, FETCH_INTERVAL
from app.db import videos_collection
logging.basicConfig(level=logging.INFO)

current_key_index = 0

def get_api_key():
    global current_key_index
    key = API_KEYS[current_key_index]
    current_key_index = (current_key_index + 1) % len(API_KEYS)
    return key


def fetch_videos(query):
    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "order": "date",
        "maxResults": 10,
        "key": get_api_key()
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return

    for item in data.get("items", []):
        video_id = item["id"]["videoId"]

        video = {
            "video_id": video_id,
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "published_at": item["snippet"]["publishedAt"],
            "thumbnail": item["snippet"]["thumbnails"]["default"]["url"]
        }

        try:
            videos_collection.update_one(
                {"video_id": video_id},
                {"$set": video},
                upsert=True
            )
        except Exception as e:
            logging.error(f"DB insert error: {e}")


def run_fetcher():
    while True:
        for q in QUERIES:
            logging.info(f"Fetching videos for: {q}")
            fetch_videos(q)

        time.sleep(FETCH_INTERVAL)
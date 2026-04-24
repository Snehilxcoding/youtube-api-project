from pymongo import MongoClient
from app.config import MONGO_URI
client = MongoClient(MONGO_URI)

db = client["youtube_db"]

videos_collection = db["videos"]

videos_collection.create_index("video_id", unique=True)
videos_collection.create_index("published_at")
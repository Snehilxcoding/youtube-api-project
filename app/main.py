from fastapi import FastAPI, Query
from app.db import videos_collection
from app.fetcher import run_fetcher

import threading

app = FastAPI()


# 🔹 Start background fetcher when server starts
@app.on_event("startup")
def start_fetcher():
    thread = threading.Thread(target=run_fetcher)
    thread.daemon = True
    thread.start()


# 🔹 Home route
@app.get("/")
def home():
    return {"message": "API is running successfully"}


# 🔹 Get videos with pagination
@app.get("/videos")
def get_videos(page: int = Query(1), limit: int = Query(10)):

    skip = (page - 1) * limit

    videos = list(
        videos_collection
        .find({}, {"_id": 0})
        .sort("published_at", -1)
        .skip(skip)
        .limit(limit)
    )

    total = videos_collection.count_documents({})

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "videos": videos
    }
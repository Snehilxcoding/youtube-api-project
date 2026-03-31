from fastapi import FastAPI, Query
from app.db import videos_collection

app = FastAPI()

# 🔹 Home route (DB test)
@app.get("/")
def home():
    return {"message": "MongoDB Connected Successfully"}


# 🔹 Insert sample data (run once manually if needed)
@app.get("/insert")
def insert_sample():
    videos_collection.insert_one({
        "video_id": "101",
        "title": "Sample Video",
        "published_at": "2026-04-01"
    })
    return {"message": "Sample data inserted"}


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


# 🔹 Delete test data (optional cleanup)
@app.get("/cleanup")
def cleanup():
    videos_collection.delete_many({"test": "connected"})
    return {"message": "Test data removed"}
from fastapi import FastAPI, Query
from db import videos_collection
from fetcher import run_fetcher
import threading

app = FastAPI()


# 🔹 Get videos with pagination + search
@app.get("/videos")
def get_videos(
    page: int = Query(1),
    limit: int = Query(10),
    query: str = Query("cricket")
):
    skip = (page - 1) * limit

    search_filter = {
        "title": {"$regex": query, "$options": "i"}
    }

    videos = list(
        videos_collection
        .find(search_filter, {"_id": 0})
        .sort("published_at", -1)
        .skip(skip)
        .limit(limit)
    )

    total = videos_collection.count_documents(search_filter)

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "videos": videos
    }


# 🔹 Root route (health check)
@app.get("/")
def home():
    return {"message": "API is running successfully"}


# 🔹 Start background fetcher + server
if __name__ == "__main__":
    t = threading.Thread(target=run_fetcher)
    t.daemon = True
    t.start()

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello Master Wayne"}

@app.get("/videos")
def get_videos(page: int = Query(1), limit: int = Query(10)):
    return {
        "page": page,
        "limit": limit,
        "videos": []
    }
    from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello Master Wayne"}

# Dummy dataset (100 videos)
dummy_videos = [
    {"id": i, "title": f"Video {i}"} for i in range(1, 101)
]

@app.get("/videos")
def get_videos(page: int = Query(1), limit: int = Query(10)):

    start = (page - 1) * limit
    end = start + limit

    paginated_data = dummy_videos[start:end]

    return {
        "page": page,
        "limit": limit,
        "total": len(dummy_videos),
        "videos": paginated_data
    }
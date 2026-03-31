from pymongo import MongoClient

# 🔴 Replace YOUR_PASSWORD and YOUR_CLUSTER_URL
MONGO_URI = "mongodb+srv://snehilxcoding:masterwayne654836@youtube-cluster.9rybgha.mongodb.net/?appName=youtube-cluster"
# Create client
client = MongoClient(MONGO_URI)

# Create / access database
db = client["youtube_db"]

# Create / access collection
videos_collection = db["videos"]
import os
from dotenv import load_dotenv

load_dotenv()

API_KEYS = os.getenv("API_KEYS").split(",")
QUERIES = os.getenv("QUERY_LIST").split(",")
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 10))
MONGO_URI = os.getenv("MONGO_URI")
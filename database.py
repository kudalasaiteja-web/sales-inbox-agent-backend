import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # reads variables from .env into the environment

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["sales_inbox_agent"]   # database name (auto-created if it doesn't exist)
tasks_collection = db["tasks"]     # like a "table" in MongoDB terms

def init_db():
    # Ping the server to confirm the connection actually works
    client.admin.command("ping")
    print("MongoDB connected.")
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv('know.env')

conn_str = os.getenv('MONGODB_URL')

client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)

mydb = MyClient["navkord"]
user_col = mydb["users"]

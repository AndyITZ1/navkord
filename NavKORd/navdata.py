from pymongo import MongoClient
import os
from dotenv import load_dotenv

#Loads in the env file containing all secured tokens.
load_dotenv('know.env')

#MongoDB URI used to connect with Atlas cluster from the application
conn_str = os.getenv('MONGODB_URL')

#Creates the connection between the application and the Atlas database
client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)

#Creates database
mydb = client["navkord"]

#Creates collection
user_col = mydb["users"]
etok_col = mydb["etok"]

#RPG Collection
#This is in the future, rpg collection will have a list of users, but this is an optional sign up meaning some users my not have data for this collection
#rpg_col = mydb["rpg"]

def add_to(results):
    etok_col.insert_one(results)


def find_db(word):
    for x in etok_col.find({ "word": word }, {"_id": False}):
        return x

def check_db(word):
    print("Checking DB for " + word)
    for x in etok_col.find({"word": word}, {"_id": False}):
        for key, value in x.items():
            if value == word:
                return True
            else:
                return False

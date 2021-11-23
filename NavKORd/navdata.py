from pymongo import MongoClient
import os
import datetime
from dotenv import load_dotenv

# Loads in the env file containing all secured tokens.
load_dotenv('know.env')

# MongoDB URI used to connect with Atlas cluster from the application
conn_str = os.getenv('MONGODB_URL')

# Creates the connection between the application and the Atlas database
client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)

# Creates database
mydb = client["navkord"]

# Creates collection
user_col = mydb["users"]
etok_col = mydb["etok"]
ktoe_col = mydb["ktoe"]


# RPG Collection
# This is in the future, rpg collection will have a list of users, but this is an optional sign up meaning some users my not have data for this collection
# rpg_col = mydb["rpg"]

class UserDB:

    def __init__(self):
        pass

    def add_user(self, user_data):
        user_col.insert_one(user_data)

    def find_user(self, user):
        user_query = user_col.find({"user": str(user)}, {"_id": False})
        for x in user_query:
            return x
        else:
            return {}

    def update_user(self, user, updated_data):
        user_col.update_one({"user": str(user)}, updated_data)


class Ktoe:

    def __init__(self):
        pass

    def add(self, results):
        ktoe_col.insert_one(results)

    def find(self, word):
        for x in ktoe_col.find({"word": word}, {"_id": False}):
            ktoe_col.update_one({"word": word},
                                {"$set": {"count": x["count"] + 1, "date": datetime.datetime.now().isoformat()}})
            return x
        return False

    def recent(self, amount):
        y = []
        total = 1
        for x in ktoe_col.find().sort("date", -1):
            y.append(x["word"])
            if total == amount:
                return y
            else:
                total += 1
        return y

    def popular(self, amount):
        y = []
        total = 1
        for x in ktoe_col.find().sort("count", -1):
            y.append(x["word"])
            if total == amount:
                return y
            else:
                total += 1
        return y

    def random(self, size):
        out = []
        for x in ktoe_col.aggregate([{"$sample": {"size": size}}]):
            if x in out:
                pass
            else:
                out.append(x)
        return out


class Etok:

    def __init__(self):
        pass

    def add(self, results):
        etok_col.insert_one(results)

    def find(self, word):
        for x in etok_col.find({"Word": word}, {"_id": False}):
            etok_col.update_one({"Word": word},
                                {"$set": {"count": x["count"] + 1, "date": datetime.datetime.now().isoformat()}})
            return x

    def recent(self, amount):
        y = []
        total = 1
        for x in etok_col.find().sort("date", -1):
            y.append(x["Word"])
            if total == amount:
                return y
            else:
                total += 1
        return y

    def popular(self, amount):
        y = []
        total = 1
        for x in etok_col.find().sort("count", -1):
            y.append(x["Word"])
            if total == amount:
                return y
            else:
                total += 1
        return y

    def check(self, word):
        print("Checking DB for " + word)
        for x in etok_col.find({"Word": word}, {"_id": False}):
            for key, value in x.items():
                if value == word:
                    return True
                else:
                    return False

    def random(self, size):
        out = []
        for x in etok_col.aggregate([{"$sample": {"size": size}}]):
            if x in out:
                pass
            else:
                out.append(x)
        return out

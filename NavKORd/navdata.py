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
# This is in the future, rpg collection will have a list of users,
# but this is an optional sign up meaning some users my not have
# data for this collection
# rpg_col = mydb["rpg"]

class UserDB:

    def __init__(self):
        pass

    # adds the user if user does not exist in the database.
    @staticmethod
    def add_user(user_data):
        user_col.insert_one(user_data)

    # finds the user and returns database info of user. Ex: gold, xp, recent search words.
    @staticmethod
    def find_user(user):
        user_query = user_col.find({"user": str(user)}, {"_id": False})
        for x in user_query:
            return x
        else:
            return {}

    # Updates user info like xp, recent search words, level.
    @staticmethod
    def update_user(user, updated_data):
        user_col.update_one({"user": str(user)}, updated_data)


class Ktoe:

    def __init__(self):
        pass

    # Will add the new search word to database
    @staticmethod
    def add(results):
        ktoe_col.insert_one(results)

    # Checks if words exist in database and will return search results.
    @staticmethod
    def find(word):
        for x in ktoe_col.find({"word": word}, {"_id": False}):
            ktoe_col.update_one({"word": word},
                                {"$set": {"count": x["count"] + 1, "date": datetime.datetime.now().isoformat()}})
            return x
        return False

    # Grabs the top recent words in a specified quantity.
    @staticmethod
    def recent(amount):
        y = []
        total = 1
        for x in ktoe_col.find().sort("date", -1):
            y.append(x["word"])
            if total == amount:
                return y
            else:
                total += 1
        return y

    # Grabs the top popular words in a specified quantity.
    @staticmethod
    def popular(amount):
        y = []
        total = 1
        for x in ktoe_col.find().sort("count", -1):
            y.append(x["word"])
            if total == amount:
                return y
            else:
                total += 1
        return y

    # Grabs the random words in a specified quantity.
    @staticmethod
    def random(size):
        out = []
        if size == 1:
            for x in ktoe_col.aggregate([{"$sample": {"size": size}}]):
                return x
        for x in ktoe_col.aggregate([{"$sample": {"size": size}}, {"$match": {"conj": {"$exists": False}}}]):
            if x in out:
                pass
            else:
                out.append(x)
        return out


class Etok:

    def __init__(self):
        pass

    # Will add the new search word to database
    @staticmethod
    def add(results):
        etok_col.insert_one(results)

    # Checks if words exist in database and will return search results.
    @staticmethod
    def find(word):
        for x in etok_col.find({"Word": word}, {"_id": False}):
            etok_col.update_one({"Word": word},
                                {"$set": {"count": x["count"] + 1, "date": datetime.datetime.now().isoformat()}})
            return x

    # Grabs the top recent words in a specified quantity.
    @staticmethod
    def recent(amount):
        y = []
        total = 1
        for x in etok_col.find().sort("date", -1):
            y.append(x["Word"])
            if total == amount:
                return y
            else:
                total += 1
        return y

    # Grabs the top popular words in a specified quantity.
    @staticmethod
    def popular(amount):
        y = []
        total = 1
        for x in etok_col.find().sort("count", -1):
            y.append(x["Word"])
            if total == amount:
                return y
            else:
                total += 1
        return y

    # Checks if words exist in database and will return search results.
    @staticmethod
    def check(word):
        print("Checking DB for " + word)
        for x in etok_col.find({"Word": word}, {"_id": False}):
            for key, value in x.items():
                if value == word:
                    return True
                else:
                    return False

    # Grabs the random words in a specified quantity.
    @staticmethod
    def random(size):
        out = []
        for x in etok_col.aggregate([{"$sample": {"size": size}}]):
            if x in out:
                pass
            else:
                out.append(x)
        return out

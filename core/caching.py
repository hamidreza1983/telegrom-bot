import redis
from pymongo import MongoClient
import json

TTL_TIME = 300
client = MongoClient("mongodb://mongodb:27017")
db = client["group2"]
collection = db["users2"]

r = redis.Redis(host='redis', port=6379, decode_responses=True)

def get_or_set_on_cache(user : dict) -> dict:
    "this fuction return user from cache"

    user_cache = r.get(str(user["id"]))
    if user_cache is not None:
        print ("from cache")
        return json.loads(user_cache)
    else:
        print ("from db")
        user_db = collection.find_one({"user_id":user["id"]})
        if user_db is None:
            collection.insert_one({"user_id":user["id"],
                                   "username":user["username"],
                                   })
            user_db_main = collection.find_one({"user_id":user["id"]})
            user_db_main.pop("_id", None)
            r.setex(str(user["id"]), TTL_TIME, json.dumps(user_db_main))
            return user_db_main
        else:
            user_db.pop("_id", None)
            r.setex(str(user["id"]), TTL_TIME, json.dumps(user_db))
            return user_db





import os

from pymongo import MongoClient

client_string = "mongodb://"+os.environ.get("MONGO_USER_ID")+":" + os.environ.get("MONGO_USER_PASS")+"@"+os.environ.get("MONGO_URL")+"/?retryWrites=true&w=majority"
client = MongoClient(client_string)
webapp = client.WebApp
users_db = webapp.users
products_db = webapp.products
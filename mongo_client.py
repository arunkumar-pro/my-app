from dotenv import load_dotenv
import os

import pymongo
load_dotenv()

database_url = os.getenv("BD_URL")

client = pymongo.MongoClient(database_url)

db = client["user_data"]
users = db["students"]
es_table = db["elastic_data"]

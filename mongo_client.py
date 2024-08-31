from dotenv import load_dotenv
import os

import pymongo
load_dotenv()

database_url = os.getenv("BD_URL")

client = pymongo.MongoClient(database_url)

db = client["user_data"]
users = db["students"]

# query = {"name": "AKvarsha"}
#
# data = col.find_one(query)
# print(data)



# Replace with your MongoDB URI
# client = pymongo.MongoClient(database_url)

# Access the admin database
# admin_db = client.admin

# Run the serverStatus command
# server_status = admin_db.command("serverStatus")

# Extract connection details
# connections = server_status.get("connections")
#
# print("Current connections:", connections.get("current"))
# print("Available connections:", connections.get("available"))
# print("Total created connections:", connections.get("totalCreated"))

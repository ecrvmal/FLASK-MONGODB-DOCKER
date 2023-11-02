import time

from pymongo import MongoClient


client = MongoClient('localhost', 27017)
# client = MongoClient('localhost', 27017, username='username', password='password')

db = client.flask_db
user = db.user
note = db.note

# class User():
#     def __init__(self):
#         self.name =""
#         self.active = True
#
# user2 = User()
# user2.name = "Ivan"
# user_data = user2.__dict__
# print(user_data)
# user.insert_one(user_data)
#
# # user.insert_one({"name": "admin", "active": "True" })
#
# user1 = user.find_one({'name':"admin"})
# print(user1)
# user_id = user1['_id']
# data = {"param1": "data1" }


note.insert_one({
    "title" : "db_init"
})

import pymongo
from pymongo import MongoClient 
import json
import os

def addArticleHandler(db, dblp, client):
    print("add")
    # one = db["dblp"].find_one()
    # print(one)
    
    # insert test
    db.dblp.insert_one({
    "_id": "636f69edfa0286ecedf58f69",
    "authors": [
      "prabh kooner",
      "Mustafa Ulutas",
      "Vasif V. Nabiyev"
    ],
    "n_citation": 0,
    "references": [
      "5626736c-e434-4e2d-8405-54940fab88ab",
      "8e87e87b-87a8-4dd2-8365-e79fbe1b4b93",
      "98f543e3-d61c-4099-ae96-237816472592",
      "99e7103c-1f1c-4ac6-8cb1-e0af35606848"
    ],
    "title": "wowie wow wow",
    "venue": "at my crib yo",
    "year": 2011,
    "id": "00701b05-684f-45f9-b281-425abfec482c"
  })
import pymongo
from pymongo import MongoClient 
import json
import os

def authorHandler(db, dblp, client):
    print("author")

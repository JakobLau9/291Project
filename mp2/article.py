import pymongo
from pymongo import MongoClient 
import json
import os

def articleHandler(db, dblp, client):
    print("article")

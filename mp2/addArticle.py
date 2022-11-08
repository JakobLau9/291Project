import pymongo
from pymongo import MongoClient 
import json
import os

def addArticleHandler(db, dblp, client):
    print("add")

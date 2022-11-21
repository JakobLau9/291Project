import pymongo
from pymongo import MongoClient 
import json
import os
from pprint import pprint

def venueHandler(db, dblp, client):
    # For each venue, list the venue, the number of articles in that venue, and the number of articles that reference a paper in that venue. 
    # Sort the result based on the number of papers that reference the venue with the top most cited venues shown first. 
    print("venue")
    return
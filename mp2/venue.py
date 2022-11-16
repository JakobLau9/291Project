import pymongo
from pymongo import MongoClient 
import json
import os
from pprint import pprint

def venueHandler(db, dblp, client):
    # For each venue, list the venue, the number of articles in that venue, and the number of articles that reference a paper in that venue. 
    # Sort the result based on the number of papers that reference the venue with the top most cited venues shown first. 
    print("venue")
    

    # number of articles in that venue
    y = db.dblp.aggregate([{"$group" : {"_id" : "$venue", "count":{"$sum":1}}}])
    
    for item in y:
        print("{} | count: {}".format(item["_id"], item["count"]))
        # store this stuff in map with venue->count
    
    
    # get a list that contains all references
    # for each ref in list
    # run a query: article in ref?? if so project the article and it's venue
    # group by venue and get the count, sort by count, and get only top n
    
    # print venue, count, and the get the other count from the map, cuz key = venue
    
    
    return
    # yikes = db.dblp.find({}, {"title":1, "venue":1, "_id":0})
    # print(yikes)
    
    # for x in yikes:
    #     pprint(x)
    
    # yikes = db.dblp.aggregate([{"$group": {"_id":{"v":"$venue"}, "num": {"$sum":1}}}])
    
    
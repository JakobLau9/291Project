import pymongo
from pymongo import MongoClient 
import json
import os
from pprint import pprint

def venueHandler(db, dblp, client):
    # For each venue, list the venue, the number of articles in that venue, and the number of articles that reference a paper in that venue. 
    # Sort the result based on the number of papers that reference the venue with the top most cited venues shown first. 
    
    #TODO: references part is not fast enough for the 1 million
    # need to make a view or write some hard query
    #TODO: maybe use projection with the group by so we don't need to for loop to print
    # maybe store the venue:count in a dictionary if we're gonna do two separate queries
    
    # number of articles in that venue
    #y = db.dblp.aggregate([{"$group" : {"_id" : "$venue", "count":{"$sum":1}}}])
    # yikes = db.dblp.aggregate([{"$group": {"_id":{"v":"$venue"}, "num": {"$sum":1}}}])

    # n = int(input("How many venues would you like to see: "))

    # test = db.dblp.aggregate([
    #     {'$match': {
    #         'venue': {
    #             '$ne':''
    #         }
    #     }},
    #     { '$group': {
    #         '_id': '$venue',
    #         'articleCount': {'$sum': 1}
    #     }
    #     },
    #     {'$sort': {'articleCount': -1}}
    # ])

    # count = 0
    # for item in test:
    #     count = count + 1
    #     if (count > n):
    #         break
    #     print(item)
    
    #for item in y:
    #    count = item["count"]
    #    v = item["_id"]
    #    print(f"{v} : {count}")
    
    
    ###### NOT FAST ENOUGH FOR THE 1 MILLION
    ##### NEED TO MAKE A VIEW OR WRTIE SOME HARD QUERY
    
    print("venue")
    yikes = db.dblp.find({}, {"id":1, "venue":1, "_id":0})
    
    ven_dict = {}
    
    for x in yikes:
        aid = x["id"]
        venue = x["venue"]
        results = db.dblp.find({"$text": {"$search": aid}})
        for article in results:
            print(article)
            ref_article_id = article["id"]
            # if (ref_article_id == aid):
            if (venue in ven_dict):
                ven_dict[venue] +=1
            else:
                ven_dict[venue] = 1

    print(ven_dict)
            
    return
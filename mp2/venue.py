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

    n = int(input("How many venues would you like to see: "))

    #test = db.dblp.aggregate([
    #   {'$match': {
    #        'venue': {
    #            '$ne':''
    #        }
    #    }},
    #    { '$group': {
    #        '_id': '$venue',
    #        'articleCount': {'$sum': 1}
    #    }
    #    },
    #    {'$sort': {'articleCount': -1}}
    #])

    #count = 0
    #for item in test:
    #    count = count + 1
    #    if (count > n):
    #        break
    #    print(item)
    
    #for item in y:
    #    count = item["count"]
    #    v = item["_id"]
    #    print(f"{v} : {count}")
 
    
    ###### NOT FAST ENOUGH FOR THE 1 MILLION
    ##### NEED TO MAKE A VIEW OR WRTIE SOME HARD QUERY
    
    #print("venue")
    #yikes = db.dblp.find({}, {"id":1, "venue":1, "_id":0})
    
    #en_dict = {}
    
    #for x in yikes:
    #    aid = x["id"]
    #    venue = x["venue"]
    #    results = db.dblp.find({"references": aid})
    #    for article in results:
    #        #print(article)
    #        #ref_article_id = article["id"]
    #        # if (ref_article_id == aid):
    #        if (venue in ven_dict):
    #            ven_dict[venue] +=1
    #        else:
    #            ven_dict[venue] = 1

    #print("\n".join("{}\t{}".format(k, v) for k, v in ven_dict.items()))
    
    # key is the venue name and value is the list of articles in that venue
    venue_articles = {}

    # key is the article being referenced and value is the list of articles that reference it
    references = {}

    for x in db.dblp.find():
        aid = x['id']

        if 'venue' in x and x['venue'] != "":
            vid = x['venue']
            if vid in venue_articles:
                venue_articles[vid].append(aid)
            else:
                venue_articles[vid] = [aid]
        else:
            continue

        if aid not in references:
            references[aid] = []

        if 'references' in x:
            referenceList = x['references']
            for y in referenceList:
                if y in references:
                    references[y].append(aid)
                else:
                    references[y] = [aid]
        else:
            continue

    
    #print("\n".join("{}\t{}".format(k, v) for k, v in venue_articles.items()))


    # The final dict will contain the venue as well as the article count and reference count
    final_dict = {}
    for key, value in venue_articles.items():
        articleCount = 0
        referenceCount = 0
        for item in value:
            articleCount += 1
            referencesAmount = len(references[item])
            referenceCount += referencesAmount
        final_dict[key] = [articleCount, referenceCount]
    
    # Sorting the dictionary by reference count
    sorted_dict = sorted(final_dict.items(), key = lambda item: item[1], reverse = True)

    # Outputting the dictionary 
    count = 0
    for key, value in sorted_dict:
        count += 1
        if (count > n):
            break
        print("Venue: " + key + " Article Count: " + str(value[0]) + " References Count: " + str(value[1]))


    return
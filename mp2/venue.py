import pymongo
from pymongo import MongoClient 
import json
import os
from pprint import pprint

def venueHandler(db, dblp, client):
    # For each venue, list the venue, the number of articles in that venue, and the number of articles that reference a paper in that venue. 
    # Sort the result based on the number of papers that reference the venue with the top most cited venues shown first. 

    n = int(input("How many venues would you like to see: "))

    # key is the venue name and value is the list of articles in that venue
    venue_articles = {}

    # key is the article being referenced and value is the list of articles that reference it
    references = {}

    for x in db.dblp.find():

        article = x['id']

        # Filing up venue articles dictionary
        if 'venue' in x:
            venue = x['venue']
            if venue in venue_articles:
                venue_articles[venue].append(article)
            else:
                venue_articles[venue] = [article]

        
        if article not in references:
            references[article] = []

        # Filling up references dictionary
        if 'references' in x:
            referencesList = x['references']

            for reference in referencesList:
                if reference in references:
                    references[reference].append(article)
                else:
                    references[reference] = [article]

    
    #print("\n".join("{}\t{}".format(k, v) for k, v in venue_articles.items()))

    # Query to get all of the venues that do not have ""
    test = db.dblp.aggregate([
       {'$match': {
            'venue': {
                '$ne':''
            }
        }},
        { '$group': {
            '_id': '$venue',
            'articleCount': {'$sum': 1}
        }
        }
    ])

    # The final dict will contain the venue as well as the article count and reference count
    final_dict = {}
    for venue in test:
        venue_name = venue['_id']
        articles = venue_articles[venue_name]
        # Used set() here to make sure we dont double count
        ref_articles = set()
        referenceCount = 0
        for article in articles:
            references1 = references[article]
            for aid in references1:
                if aid not in ref_articles:
                    referenceCount += 1
                    ref_articles.add(aid)
        final_dict[venue_name] = [referenceCount, venue["articleCount"]]
    
    # Sorting the dictionary by reference count
    sorted_dict = sorted(final_dict.items(), key = lambda item: item[1], reverse = True)

    # Outputting the dictionary 
    count = 0
    for key, value in sorted_dict:
        count += 1
        if (count > n):
            break
        print("Venue: " + key + " Article Count: " + str(value[1]) + " References Count: " + str(value[0]))


    return
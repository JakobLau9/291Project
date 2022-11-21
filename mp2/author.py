import pymongo
from pymongo import MongoClient 
import json
import os

def authorHandler(db, dblp, client):
    # print("author")
    keyword = input("Please enter a keyword: ")
    # keyword = "merlo"
    # search_term = ""
    # search_term += "\\"
    # search_term += keyword
    # search_term += "\\"
    
    search_term = '"' + keyword + '"'
    
    results = db.dblp.find({"$text": {"$search": search_term}}, {"authors": 1})
    author_dict = {}
    
    for item in results:
        mylist = list(item["authors"])
        # print(*mylist, sep = ", ")
        filter_object = filter(lambda a: keyword.lower() in a.lower(), mylist)
        # all authors that match in one article 
        # usually just 1 will match in a single article unless coauthors have the same name
        author_match = list(filter_object)
        for author in author_match:
            if (author in author_dict):
                author_dict[author] +=1
            else:
                author_dict[author] =1
    
    # now we have the author name and the number of publications
    # stored as a map so like bob:1
    print(author_dict)
    return



# can't get elem match to work
# data = db.dblp.find({"authors": { "$elemMatch": "Tim"} })

# starting with something like this might be faster LOL OOPS
# but with match instead of find cuz we need aggregation for sorting
# data = db.dblp.find( { "authors": "Tim" } 

def authorSelect(db, dblp, client):
    # The user should be able to select an author and see the title, year and venue of all articles by that author. 
    # The result should be sorted based on year with more recent articles shown first.
    
    keyword = input("Please enter a name: ")
    # keyword = "merlo"
    # search_term = ""
    # search_term += "\\"
    # search_term += keyword
    # search_term += "\\"
    # results = db.dblp.find({"$text": {"$search": search_term}})
    
    search_term = '"' + keyword + '"'
    
    results = (db.dblp.aggregate([
        {"$match": {"$text": {"$search": search_term}}},
        # {"$project": {"authors":1}},
        {"$sort": {"year": -1}}]))
    
    

    for item in results:
        mylist = list(item["authors"])
        # print(*mylist, sep = ", ")
        # this time we will only have one exact match
        if keyword in mylist:            
            title = item["title"]
            year = item["year"]
            venue = item["venue"]
            print(f"title: {title}, year: {year}, venue: {venue}")

    return
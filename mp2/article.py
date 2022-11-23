import pymongo
from pymongo import MongoClient 
from pprint import pprint
import json
import os

def articleHandler(db, dblp, client):
    print("article")
    keywords = input("Please enter one or more unique keywords (comma-separated)\n")
    keywords_list = keywords.split(",")

    # format the keywords as a phrase searches so they are effectively ANDED
    search_str = ""
    for word in keywords_list:
        search_str += "\"" + word + "\" "
    search_str.strip()
    
    # this will return an article where all the keywords match
    results = db.dblp.find({"$text": {"$search": search_str}}, {"_id":0, "id": 1, "title": 1, "year": 1, "venue": 1})
    
    for item in results:
        pprint(item) #pretty print
    return




def selectArticle(db, dblp, client):
    selection = input("select an article by id: ")
    # we have unique index on id so this is good i think
    data = db.dblp.find({"id": selection}, {"_id":0, "references": 0})
    
    # display everything except references
    for item in data:
        pprint(item)
    
    search = f'"{selection}"'
    print("--------------articles that reference selected article--------------")
    # don't know if it references should have a text index or not
    # search all references arrays for this article id
    # if this id is found in a ref array display the otherh articles information
    refby = db.dblp.find({"$text": {"$search": search}}, {"_id":0, "id": 1, "title": 1, "year": 1}) 
    for i in refby:
        print(i)
    return
                       
                       
                       
                       
                         
                         
    # data = db.dblp.find( { "references": article_id } )
    # for result in data:
    #     ref_id = result["id"]
    #     ref_title = result["title"]
    #     ref_year = result["year"]
    #     print(f"id: {ref_id}, title: {ref_title}, year: {ref_year}")
    # print("-----------------------------------------------")
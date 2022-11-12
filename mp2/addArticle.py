import pymongo
from pymongo import MongoClient 
import json
import os

def addArticleHandler(db, dblp, client):
    # TODO: error checking, checking if id is unique??
    
    # user provides id, title, list of authors, year
    # add the new article to the collection
    # The fields abstract and venue should be set to null, 
    # references should be set to an empty array and n_citations should be set to zero.
    
    
    unique_id = input("Please enter an id: ")
    title = input("Please enter a title: ")
    authors = input("Please enter a space separated list of authors: ")
    year = input("Please enter a year: ")
    
    author_list = authors.split()
    #id example 00701b05-684f-45f9-b281-425abfec482c

    
    db.dblp.insert_one({
    "abstract": None,
    "authors": author_list,
    "n_citation": 0,
    "references": [],
    "title": title,
    "venue": None,
    "year": year,
    "id": unique_id})
    
    print("article successfully inserted")
    return
import pymongo
from pymongo import MongoClient 
import json
import sys
import os
db = None
dblp = None
client = None

import venue
import addArticle
import article
import author



def main():
    global db
    global dblp
    global client
    
    # python3 phase2.py port
    # python3 phase2.py 27017
    
    port = sys.argv[1]
    
    client = MongoClient("mongodb://localhost:" + port)
    db = client["291db"]
    dblp = db["dblp"]
    
    cmds = '''
        search for articles
        search for authors
        list venues
        add an article
        exit
        '''
    
    print("Enter 'command' to see details")
    
    while True:
        command = input("Please enter a command: ")
        if (command == "command"):
            print(cmds)
        
        elif (command == "search for articles"):
            article.articleHandler(db, dblp, client)
            
        elif (command == "search for authors"):
            author.authorHandler(db, dblp, client)
            
        elif (command == "list venues"):
            venue.venueHandler(db, dblp, client)
            
        elif (command == "add an article"):
            addArticle.addArticleHandler(db, dblp, client)
        elif (command == "exit"):
            break
        
        else:
            print("invalid")

if __name__ == "__main__":
    main()
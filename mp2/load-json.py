import pymongo
from pymongo import MongoClient 
import json
import os
db = None
dblp = None
client = None

import venue
import addArticle
import article
import author

def createCollection():
    # TODO: port number is hardcoded cuz i don't want to type it everytime, we'll change at the end
    # TODO: json file name is hardcoded cuz im lazy
    
    port = input("Enter port number: ") # 27017 is default server
    client = MongoClient("mongodb://localhost:" + "27017")
    
    db = client["291db"]
        
    # create collection dblp unless it already exists
    collist = db.list_collection_names()
    if "dblp" in collist:
        print("dblp collection already exists: recreating ...")
        db["dblp"].drop()
    else:
        dblp = db["dblp"]
        
    # insert json file data into collection
    
    # TODO: don't know if this is allowed seems too clean
    # wowie wow im so clean
    cmd = "mongoimport --db 291db --collection dblp --file dblp-ref-1k.json --batchSize 1"
    os.system(cmd)

def main():
    createCollection()
    print("data imported successfully")
    
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
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

def createCollection():
    global db
    global dblp
    global client
    # TODO: port number is hardcoded cuz i don't want to type it everytime, we'll change at the end
    # TODO: json file name is hardcoded cuz im lazy
    
    file_name = sys.argv[1] # example: dblp-ref-10.json
    port = sys.argv[2] # example: 27017
    
    client = MongoClient("mongodb://localhost:" + port)
    
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
    cmd = f"mongoimport --db 291db --collection dblp --file {file_name} --batchSize 1"
    os.system(cmd)
    
    

def main():
    # python3 load-json.py file.json port
    # python3 load-json.py dblp-ref-10.json 27017
    
    createCollection()
    print("data imported successfully")
    client.close()
    
if __name__ == "__main__":
    main()
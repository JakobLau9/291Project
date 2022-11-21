import pymongo
from pymongo import MongoClient
from pymongo import TEXT
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
    # insert json file data into collection
    print("importing ...")
    cmd = f"mongoimport --port {port} --db 291db --collection dblp --file {file_name} --batchSize 100"
    os.system(cmd)
    
    
    
    # create indexes
    db.dblp.drop_indexes()
    print("creating indexes ...")
    
    # db.dblp.create_index([('authors', TEXT)], name='author_index')
    
    # we can only have 1 text index
    # this is ok for search for articles
    # for search for authors you need to get rid of the other text matches
    db.dblp.create_index([('authors', TEXT), ('title', TEXT), ('abstract', TEXT), ('venue', TEXT), ('year', TEXT)], name='author_index')
    
    #unique id index for add article checking
    db.dblp.create_index( "id", unique=True, name='uniq_id_index' )
    
    # displaying all indexes
    info = db.dblp.index_information()
    for i in info:
        print(i)

def main():
    # python3 load-json.py file.json port
    # python3 load-json.py dblp-ref-10.json 27017
    
    createCollection()
    print("data imported successfully")
    client.close()
    
if __name__ == "__main__":
    main()
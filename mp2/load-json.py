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
    
    if len(sys.argv) != 3:
        print("Please follow the format: python3 load-json.py <json file> <port>")
        quit()

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
    cmd = f"mongoimport --port {port} --db 291db --collection dblp --file {file_name} --batchSize 100000"
    os.system(cmd)
    
    
    
    # create indexes
    db.dblp.drop_indexes()
    print("creating indexes ...")
    # db.dblp.create_index("references", name='ref_index')
    #unique id index for add article checking
    # db.dblp.create_index( "id", unique=True, name='uniq_id_index' )
    print("created unique id index")
    db.dblp.create_index([('authors', TEXT), ('title', TEXT), ('abstract', TEXT), ('venue', TEXT), ('references', TEXT)], name='author_index')
    print("created text index")
    # change year to string so we can text search on it
    db.dblp.update_many(filter={ }, update=[{'$set': {'year': { '$toString': '$year'}}}], upsert=False)
    print("converted year")
    
    
    
    
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
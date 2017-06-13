#Funtions to fill the database with json collections: articles_doc (= json with all info for abstracts_, cooccurence_doc10
# (= json file for the cooccurence graph, sunburst_doc10 (= json fil for sunbust diagram)
from pymongo import MongoClient
import pickle
import simplejson as json

#specify client and database
client = MongoClient()
db = client.TextGraver

#push json files to Mongo database
def fill_database():

    #read articles_doc and load to json format
    articles_doc = open("articles_doc.json")
    articles_doc_buffer = articles_doc.read()
    articles_doc_json = json.loads(articles_doc_buffer)

    collection_articles = db.articles
    db.collection_articles.delete_many({})

    #read graaf_doc and load to json format
    graaf_doc = open("cooccurence_doc10.json")
    graaf_doc_buffer = graaf_doc.read()
    graaf_doc_json = json.loads(graaf_doc_buffer)

    collection_graaf = db.graaf
    db.collection_graaf.delete_many({})

    #read sunburst_doc and load to json format
    sunburst_doc = open("sunburst_doc10.json")
    sunburst_doc_buffer = sunburst_doc.read()
    sunburst_doc_json = json.loads(sunburst_doc_buffer)

    collection_sunburst = db.sunburst
    db.collection_sunburst.delete_many({})

    #insert json formats into database collections
    for article in articles_doc_json:
        collection_articles.insert(article, check_keys = False)

    for graaf in graaf_doc_json:
        collection_graaf.insert(graaf, check_keys = False)

    for sunburst in sunburst_doc_json:
        collection_sunburst.insert(sunburst, check_keys = False)


def main():
    fill_database()

main()
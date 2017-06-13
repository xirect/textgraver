from pymongo import MongoClient
import pickle
import simplejson as json

def fill_database():
    client = MongoClient()
    db = client.TextGraver


    articles_doc = open("../articles_doc.json")
    articles_doc_buffer = articles_doc.read()
    articles_doc_json = json.loads(articles_doc_buffer)

    collection_articles = db.articles
    db.collection_articles.delete_many({})

    graaf_doc = open("../cooccurence_doc10.json")
    graaf_doc_buffer = articles_doc.read()
    graaf_doc_json = json.loads(graaf_doc_buffer)

    collection_graaf = db.graaf
    db.collection_graaf.delete_many({})

    sunburst_doc = open("../sunburst_doc10.json")
    sunburst_doc_buffer = articles_doc.read()
    sunburst_doc_json = json.loads(sunburst_doc_buffer)

    collection_sunburst = db.sunburst
    db.collection_sunburst.delete_many({})

    for article in articles_doc_json:
        collection_articles.insert(article, check_keys = False)

    for graaf in graaf_doc_json:
        collection_graaf.insert(graaf, check_keys = False)

    for sunburst in sunburst_doc_json:
        collection_sunburst.insert(sunburst, check_keys = False)

def main():
    fill_database()

main()

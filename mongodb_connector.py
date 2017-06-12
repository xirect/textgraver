from pymongo import MongoClient
import pickle
import simplejson as json

client = MongoClient()
db = client.testdb

articles_doc = pickle.load(open('demo/ncbi_api_articles_doc.p', 'rb'))
articles_doc = json.loads(articles_doc)

collection = db.test
collection2 = db.graaf


for article in articles_doc:
    collection.insert(article)

query = {
    "species": "Arabidopsis thaliana",
    "chemicals" :"Anthocyanin"


}
results = collection.find(query)
for doc in results:
    print(doc)

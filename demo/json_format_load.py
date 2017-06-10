import simplejson as json
import pickle


def main():
    articles_doc = pickle.load(open('ncbi_api_articles_doc.p', 'rb'))

    articles_doc = json.loads(articles_doc)

    for article in articles_doc:
        print(article)
        
main()
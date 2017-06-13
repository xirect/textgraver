#Functions for retrieving EggNOG ID to
from pymongo import MongoClient
import simplejson as json
import requests

uni_url = 'http://www.uniprot.org/uploadlists/'
eggnog_url = 'http://eggnogapi.embl.de/nog_data/html/tree/{}'

client = MongoClient()
db = client.TextGraver
def main():

    gene_name = 'SOD'
    get_uniprot_ids(gene_name)

def get_uniprot_ids(gene_name):

    cursor = db.articles.find({'species.genes.name': gene_name}, {"species": 1, "genes": 1, "uniprot_ids": 1})

    uniprot_ids = cursor

    eggnogid = fetch_eggnog_id(uniprot_ids)
    html = fetchtree(eggnogid)

def fetch_eggnog_id(uniprot_ids):

    for id in uniprot_ids:

        payload_to_eggnog = {
            'from': 'ID',
            'to': 'EGGNOG_ID',
            'format': 'list',
            'query': id
        }
        # Uses the predefined parameters to request uniprot to translate an uniprot id to an eggnog id
        eggnog_id_request = requests.get(uni_url, params=payload_to_eggnog)

        # Builds a list based on the uniprot api results
        eggnog_id_text = eggnog_id_request.text
        eggnog_id_list = eggnog_id_text.split()

        # Checks if the list with eggnog id's isn't empty.
        if eggnog_id_list:
            # writes the results to a file, should be replaced by JSON logic
            eggnog_id = eggnog_id_list[0]

    return  eggnog_id


def fetchtree(eggnogid):

    r = requests.get(eggnog_url.format(eggnogid))
    html = r.content

    return html



main()







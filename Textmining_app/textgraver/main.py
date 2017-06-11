import simplejson as json
from datetime import datetime
import pickle
import entrez_api
import ncbi_ccb_api
import regex_genes
import id_mapper_eggnog
import orthodb_api
import search_terms
import sunflare



def main():
    #print(datetime.time(datetime.now()))

    #idlist, articles_doc = entrez_api.pm_ids()

    print(datetime.time(datetime.now()))

    #articles_doc = ncbi_ccb_api.ncbi_gene(idlist, articles_doc)

    #print(datetime.time(datetime.now()))

    articles_doc = pickle.load(open('articles_doc_ncbi_api_1024.p', 'rb'))


    articles_doc = regex_genes.get_regex_genes(articles_doc)

    articles_doc = id_mapper_eggnog.species_identifier(articles_doc)

    pickle.dump(articles_doc, open('articles_doc_idmapper_1024.p', 'wb'))

    print(datetime.time(datetime.now()))


    articles_doc = orthodb_api.get_orthodb_orthologs(articles_doc)

    print(datetime.time(datetime.now()))

    pickle.dump(articles_doc, open('orthodb_articles_doc_1024.p', 'wb'))

    articles_doc, cooccurence_doc = search_terms.search_terms(articles_doc)

    sunflare_doc = sunflare.construct_stress_sunflare(articles_doc)

    sunflare_doc = json.dumps(sunflare_doc)

    file = open('sunburst_doc10.json', 'w')
    file.write(sunflare_doc)
    file.close()

    cooccurence_doc = json.dumps(cooccurence_doc)

    file2 = open('cooccurence_doc10.json', 'w')
    file2.write(cooccurence_doc)
    file2.close()


main()


"""
sample json format

articles = [
   {  "pmid":"28534253",
      "title":"High throughput ST08 gene..",
      "author":["Lucas, J", "Salanter, A"],
      "source":"Journal of biomedical, Atlanta, 2008",
      "date":"20170809",
      "abstract":"Way too much text",
      "species":[{"name":"olifant","genes":[{
                  "name":"tnf-a",
                  "eggnog_id":"EGNOG8930",
                  "orthologs":{
                     "tnf-b":"solanum",
                     "tnf-c":"burbur"}}]}
      ],
      "chemicals":[
         "anthocyanin"
      ],
      "stress":[
         "salt",
         "cold"
      ],
      "correlation":[
         "increase"
      ],
      "cultivation":[
         "in vivo"
      ]
   }
]
"""
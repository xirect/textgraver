#Application for textmining of Pubmed articles with the search terms 'anthocyanin' and 'stress' to find relations
#between these two variables in plants, the application retrieves genes, chemicals and organims from the abstracts
#and retrieves additional information such as orthologs from the genes.
#Information is pushed to a MongoDB, a webapplication visualises the data in a sunburst and a cooccurence graph
#TextGraver version 1.00
#Date: 13/06/2017
#Authors: Jeffrey Hiraki, Jasper de Meijer, Heleen Severin, Sanne Geraerts
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
    print(datetime.time(datetime.now()))

    idlist, articles_doc = entrez_api.pm_ids()

    print(datetime.time(datetime.now()))

    articles_doc = ncbi_ccb_api.ncbi_gene(idlist, articles_doc)

    print(datetime.time(datetime.now()))

    records = json.loads(articles_doc)

    articles_doc = regex_genes.get_regex_genes(articles_doc)

    records = json.loads(articles_doc)

    articles_doc = id_mapper_eggnog.species_identifier(articles_doc)

    print(datetime.time(datetime.now()))

    articles_doc = orthodb_api.get_orthodb_orthologs(articles_doc)

    print(datetime.time(datetime.now()))

    articles_doc, cooccurence_doc = search_terms.search_terms(articles_doc)

    sunflare_doc = sunflare.construct_stress_sunflare(articles_doc)

    sunflare_doc = json.dumps(sunflare_doc)

    #articles_doc = json.dumps(articles_doc)

    file_articles = open('articles_doc.json', 'w')
    file_articles.write(articles_doc)
    file_articles.close()

    pickle.dump(articles_doc, open('articles_doc_pickle.p', 'wb'))

    file_sunburst = open('sunburst_doc10.json', 'w')
    file_sunburst.write(sunflare_doc)
    file_sunburst.close()

    pickle.dump(sunflare_doc, open('sunburst_doc_pickle.p', 'wb'))

    file_cooccurence = open('cooccurence_doc10.json', 'w')
    file_cooccurence.write(cooccurence_doc)
    file_cooccurence.close()

    pickle.dump(cooccurence_doc, open('cooccurence_doc_pickle.p', 'wb'))


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
#make request to NCBI for the gene, chemical and organism indices for the corresponding PMED ID
import simplejson as json
import requests
from datetime import datetime
from time import sleep

logfile = open('logile_ncbi_api', 'a')
def ncbi_gene(idlist, articles_doc):

    articles_doc = json.loads(articles_doc)
    articles_doc_update = list()

    for article in articles_doc:
        attempts = 0
        go = True
        method = 'get'
        get_method = True
        while go:
            try:
                pmid = article['pmid']
                custom_url = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/bioconcept/{}/JSON".format(pmid)
                if method == 'get':
                    r = requests.get(custom_url)
                else:
                    r = requests.post(custom_url)
                json_article = r.json()
                article_update = parse_json(json_article, article)
                articles_doc_update.append(article_update)
                go = False
            except json.JSONDecodeError:
                    go = False
            except requests.ConnectTimeout:
                attempts += 1
            except requests.ConnectionError:
                attempts += 1
            except requests.HTTPError:
                attempts += 1
            finally:
                if attempts > 2:
                    sleep(3)
                elif attempts > 3:
                    logfile.write('Connection ERROR getting orthologs for ' + '\n')
                    go = False

    logfile.close()
    articles_doc_update = json.dumps(articles_doc_update)
    return articles_doc_update


def parse_json(json_article, article):

    genes = []
    chemicals = []
    abstract = ""

    abstract = json_article['text']

    for denot in json_article['denotations']:
        if denot['obj'].split(":")[0] == 'Gene':
            genes.append([denot['span']['begin'],denot['span']['end']])
        if denot['obj'].split(":")[0] == "Chemical":
            chemicals.append([denot['span']['begin'],denot['span']['end']])

    if len(genes) == 0:
        genes.append([])
    if len(chemicals) == 0:
        chemicals.append([])

    indices = [genes, chemicals]

    article_update = pull_info_abstract(indices, abstract, article)

    return article_update


def pull_info_abstract(indices, abstract, article):

    genes = indices[0]
    chemicals = indices[1]

    genes_doc = []
    for gene in genes:
        if len(gene) != 0:
            gene_doc = {}
            start = gene[0]
            end = gene[1]
            gene_doc['name'] = abstract[start:end]
            gene_doc['orthologs'] = []
            gene_doc['eggnog'] = ''
            genes_doc.append(gene_doc)
    chemicals_doc = []
    for chemical in chemicals:
        if len(chemical) != 0:
            start = chemical[0]
            end = chemical[1]
            chemicals_doc.append(abstract[start:end])

    article['abstract'] = abstract
    article['genes'] = genes_doc
    article['chemicals'] = chemicals_doc

    return article




#Module for getting a list containing the PUBMED ID's with a hit on anthocyanin and stress
import simplejson as json
from Bio import Entrez
from Bio import Medline

def pm_ids():
    Entrez.email = "severin@student.han.nl"     # Always tell NCBI who you are
    handle = Entrez.egquery(term="anthocyanin stress")
    record = Entrez.read(handle)
    # for row in record["eGQueryResult"]:
    #     if row["DbName"]=="pubmed":
    #          print(row["Count"])

    handle = Entrez.esearch(db="pubmed", term="anthocyanin stress", retmax=8000)
    record = Entrez.read(handle)
    idlist = record["IdList"]

    handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline",
                           retmode="text")
    records = Medline.parse(handle)

    records = list(records)

    print(len(records))

    articles = list()


    for record in records:
        pmid = record.get("PMID", "?")
        title = record.get("TI", "?")
        author = record.get("AU", "?")
        source = record.get("SO", "?")
        date = record.get("EDAT", "?")

        articles.append({
            'pmid': pmid,
            'title': title,
            'author': author,
            'source': source,
            'date': date,
            'abstract': '',
            'genes': [],
            'species': [],
            'chemicals': [],
            'stress': [],
            'correlation': [],
            'cultivation': []
        })

    articles = json.dumps(articles)

    return idlist, articles
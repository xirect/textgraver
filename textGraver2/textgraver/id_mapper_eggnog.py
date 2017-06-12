import requests
from time import sleep
import simplejson as json

logfile = open('idmapper_logfile.txt', 'a')
file = open('speclist.txt', 'r')
spec_file = file.read().splitlines()
eggnog_url = 'http://eggnogapi.embl.de/nog_data/html/tree/{}'

#Function for translating gene names to eggnog id's (via uniprot idmapper)
def species_identifier(articles_doc):
    #Defining the api URL
    uni_url = 'http://www.uniprot.org/uploadlists/'
    #Loading the gene file, should be replaced by JSON logic
    articles_doc = json.loads(articles_doc)
    #Loading the all plants file which contains all (by uniprot) known abbrevations
    #for plants.
    species_file = open("all_plants.txt")
    species_lines = species_file.read().splitlines()


    #Creates a file to save the aquired data, should be replaced by JSON logic




    attempt = 0
    #Loops over the list of genes and requests uniprot to translate the genename to uniprot id's
    for a, article in enumerate(articles_doc):
        #print(a)
        genes = [x['name'] for x in article['genes']]
        for n, gene in enumerate(genes):
            go = True
            while go:
                try:
                    counter = n
                    #Defining parameters for the uniprot api
                    payload = {
                    'from': 'GENENAME',
                    'to': 'ID',
                    'format': 'list',
                    'query': gene
                    }
                    uniprot_id_request = requests.get(uni_url, params= payload)
                    text1 = uniprot_id_request.text
                    textsplit = text1.split()
                    #check is used to check if a result needs to be saved or not.

                    #Loops over the list of uniprot id's and checks if it is in the list of plants
                    #if it is in the list of plants it wil request uniprot to translate the uniprot id to an eggnog id and save this result.
                    #It will only save the first result which is a plant and has a eggnog id.

                    if textsplit is not None or len(textsplit) != 0:
                        uniprot_ids = []
                        for x in textsplit:
                            species = x.split("_")[1]
                            #Checks if it is a plant and if there aint a result for the genename yet.
                            if species in species_lines:
                                uniprot_ids.append(x)
                        update_json_record(uniprot_ids, gene, species, article)

                    go = False
                except requests.ConnectionError:
                    go = True
                    attempt += 1
                except requests.ConnectTimeout:
                    go = True
                    attempt += 1
                except requests.HTTPError:
                    go = True
                    attempt += 1
                finally:
                    if attempt > 2:
                        sleep(3)
                    elif attempt > 3:
                        logfile.write('ERROR for ' + gene + " in: " + article['pmid'] + '\n')
                        go = False
    logfile.close()
    return articles_doc

def update_json_record(uniprot_ids, gene, species, article):

    binominal = fetch_full_species(species)

    gene_doc = {'name': gene, 'orthologs':{}, 'uniprot_ids': uniprot_ids}
    species = article['species']
    all_species = [x['name'] for x in species]
    if binominal in all_species:
        for n, spec in enumerate(species):
            if species[n]['name'] == binominal:
                species_doc = species[n]
    else:
        species_doc = {'name': binominal, 'genes': []}
        species.append(species_doc)
    genes = species_doc['genes']
    all_genes = [x['name'] for x in genes]
    if gene not in all_genes:
        genes.append(gene_doc)



def fetch_full_species(species):

    for line in spec_file:
        if species and "N=" in line:
            binominal = line.split("N=")[1].strip()
    if binominal is None:
        binominal = species

    return binominal

def fetch_tree_html(eggnog_id):

    r = requests.get(eggnog_url.format_map(eggnog_id))
    html = r.content

    file = open('treehtml.html', 'w')
    file.write(str(html))
    file.close()
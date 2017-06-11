import simplejson as json
import re

correlation_terms = {"increase": "increase", "enhance": "increase", "induce": "increase", "rise": "increase",
                     "increase": "accumulation",
                     "reduction": "decrease", "decrease": "decrease", "lessen": "decrease", "decline": "decrease",
                     "declining": "decrease",
                     "positive correlated": "positive", "positively": "positive", "positively regulated": "positive",
                     "positive association": "positive",
                     "negatively": "negative", "negatively correlated": "negatative",
                     "negatively regulated": "negative", "negative association": "negative"}
stress_terms = {"drought": "drought", " dry ": "drought", "dehydrate": "drought", "osmotic": "osmotic",
                "water": "osmotic",
                "salinity": "salinity", "salin": "salinity", "acidity": "acidity", "salt": "salinity",
                "high temperature": "high temperature", "high-temperature": "high temperature",
                "heat": "high temperature",
                "low temperature": "low temperature",
                "low-temperature": "low temperature", "chilling": "low temperature", "cold": "low temperature",
                "freezing":
                    "low temperature",
                "high-light": " high light", "high light": " high light", "low-light": "low light",
                "dark-treatment": "low light", "dark exposure": "low light",
                "darkness": "low light", "oxidative": "oxidative", "ultraviolet": "ultraviolet", "UV": "ultraviolet"}
cultivation_terms = {"in vivo": "in vivo", "cultivar": "cultivar", "green-house": "cultivar", "in vitro": "in vitro",
                     "in-vitro":
                         "in vitro", "ornamental": "house plant"}


def search_terms(articles_doc):

    # dit werktarticles_doc = json.loads(json.dumps(articles_doc))
    articles_doc = json.loads(articles_doc)
    cooccurence_doc = []

    for article in articles_doc:
        abstract = article['abstract']
        correlations = list()
        for correlation in correlation_terms:
            found = abstract.find(correlation)
            if found != -1:
                correlations.append(correlation_terms.get(correlation))
        stresses = list()
        for stress in stress_terms:
            found = abstract.find(stress)
            if found != -1:
                stresses.append(stress_terms.get(stress))
        cultivations = list()
        for condition in cultivation_terms:
            found = abstract.find(condition)
            if found != -1:
                cultivations.append(cultivation_terms.get(condition))
        article['correlation'] = correlations
        article['stress'] = stresses
        article['cultivation'] = cultivations

        cooccurence_doc = cooccurence(article, correlations, stresses, cultivations, cooccurence_doc)

    articles_doc = json.dumps(articles_doc)
    cooccurence_doc = json.dumps(cooccurence_doc)

    return articles_doc, cooccurence_doc


def cooccurence(article, correlations, stresses, cultivations, cooccurence_doc):

    genes = []
    for s, species in enumerate(article['species']):
        for gene in article['species'][s]['genes']:
            genes.append(gene['name'])
    species = [x['name'] for x in article['species']]
    chemicals = article['chemicals']

    abstract = article['abstract']
    lines = re.split(r' *[\.\?!] [A-Z0-9]', abstract)

    correlation_indices = {}
    stress_indices = {}
    cultivation_indices = {}
    gene_indices = {}
    species_indices = {}

    for n, line in enumerate(lines):
        for cor in correlations:
            cor_index = line.find(cor)
            if cor_index != 0:
                correlation_indices[cor] = n
        for stress in stresses:
            stress_index = line.find(stress)
            if stress_index != 0:
                stress_indices[stress] = n
        for cult in cultivations:
            cultivation_index = line.find(cult)
            if cultivation_index != 0:
                cultivation_indices[cult] = n
        for gene in genes:
            gene_index = line.find(gene)
            if gene_index != 0:
                gene_indices[gene] = n
        for spec in species:
            species_index = line.find(spec)
            if species_index != 0:
                species_indices[spec] = n


    for gene in gene_indices:
        for species in species_indices:
            cooccurence_doc = check_cooccurence(cooccurence_doc, gene, species, gene_indices, species_indices, correlation_indices)
        for stress in stress_indices:
            cooccurence_doc = check_cooccurence(cooccurence_doc, gene, stress, gene_indices, stress_indices, correlation_indices)
        for cultivation in cultivation_indices:
            cooccurence_doc = check_cooccurence(cooccurence_doc, gene, cultivation, gene_indices, cultivation_indices, correlation_indices)
    for spec in species_indices:
        for stress in stress_indices:
            cooccurence_doc = check_cooccurence(cooccurence_doc, spec, stress, species_indices, stress_indices, correlation_indices)
        for cultivation in cultivation_indices:
            cooccurence_doc = check_cooccurence(cooccurence_doc, spec, cultivation, gene_indices, cultivation_indices, correlation_indices)
    for stress in stress_indices:
        for cultivation in cultivation_indices:
            cooccurence_doc = check_cooccurence(cooccurence_doc, stress, cultivation, stress_indices, cultivation_indices, correlation_indices)

    return cooccurence_doc

def check_cooccurence(cooccurence_doc, term1, term2, term1_indices, term2_indices, correlation_indices):
    term1_index = term1_indices.get(term1)
    term2_index = term2_indices.get(term2)

    score = 10
    if term1_index == term2_index:
        score = 30
        for correlation in correlation_indices:
            if correlation_indices[correlation] == term1_index:
                if correlation_terms.get(correlation) in ['increase', 'positive']:
                    score += 1
                elif correlation_terms.get(correlation) in ['decrease', 'negative']:
                    score -= 5
    type = determine_type(score)

    present = False
    for cooccurence in cooccurence_doc:
        if cooccurence['source'] == term1 and cooccurence['target'] == term2 or \
           cooccurence['source'] == term2 and cooccurence['target'] == term1:
            cooccurence['type'] = type
            present = True
    if not present:
        cooccurence_doc.append({'source': term1, 'target': term2, 'type': type})

    return cooccurence_doc

def determine_type(score):

    if score < 50:
         type = "gray"
    elif score in range(50,200):
        type = "green"
    elif score in range(200,500):
        type = "blue"
    elif type in range(500,800):
        type = "purple"
    else:
        type = "red"

    return type





import simplejson as json
import re

def get_regex_genes(articles_doc):

    articles_doc = json.loads(articles_doc)
    articles_doc = articles_doc

    for article in articles_doc:
        abstract = article['abstract']
        words = abstract.split()
        for word in words:
            split = split_chars(word)
            for word in split:
                if len(word) > 1 and (word[-1] == "," or word[-1] == "-"):
                    word = word[:-1]
                if len(word) > 1 and word[0] == "-":
                    word = word[1:]
                if (hasNumbers(word) or hasLowerUpper(word)) and upperLimit(word) and unwanted(word):
                    api_genes = [x['name'].lower() for x in article['genes']]
                    if word.lower() not in api_genes:
                        genes = article['genes']
                        genes.append({'name': word, 'orthologs': {}, 'eggnog': ''})

    articles_doc = json.dumps(articles_doc)
    return articles_doc


def hasNumbers(inputString):
    boolean = False
    if re.search(r'\d', inputString) and (re.search(r'([A-Za-z])', inputString)):
        boolean = True
    return boolean

def hasLowerUpper(inputString):
    boolean = False
    if re.search(r'([A-Za-z])+([A-Z])+([a-z])*(.)*', inputString):
        boolean = True
    return boolean

def upperLimit(inputString):
    boolean = False
    if inputString.isupper():
        if re.match(r'[A-Z]{3,5}$', inputString):
            boolean = True
    else:
        boolean = True
    return boolean

def split_chars(inputString):
    output = re.findall(r'[\w\',-]+', inputString)
    return output

def unwanted(inputString):
    boolean = True
    unwanted = ['induced', 'targeted', 'treated', 'involved', 'pretreated', 'negative', 'positive', 'insensitive',
                'dependent', 'independent', 'involved', 'control','scavenging', 'derived', 'protein', 'related', 'like',
                'mediated', 'related', 'responsive', 'enriched', 'overexpressing', 'governed', 'sensitive', 'absorbing',
                'produced', 'producing', 'associated', 'attributed', 'inflicted', 'ínitiated', 'elicited', 'activated',
                'supplemented', 'supplemental', 'repeat', 'enriched', 'damaging', 'signaling', 'deficient', 'guided']
    words = inputString.split('-')
    for word in words:
        if word.lower() in unwanted:
            boolean = False

    return boolean
import simplejson as json

stress_terms = ["drought", "osmotic", "salinity", "acidity", "high temperature", "low temperature", "high light", "low light", "oxidative", "ultraviolet"]

def construct_sunflares(articles_doc):

    #articles_doc = json.loads(articles_doc)
    stress_sunflare = construct_stress_sunflare(articles_doc)
    #species_sunflare = construct_species_sunflare(articles_doc)

    stress_sunflare = json.dumps(stress_sunflare)

    return stress_sunflare


def construct_stress_sunflare(articles_doc):
    sunflare = {"name": "Hits",
                "description": "All the hits found",
                "children": [{"name": "Stressomstandigheden", "description": "All the different stresses",
                              "children": []}]}

    sunflare = json.loads(json.dumps(sunflare))
    articles_doc = json.loads(articles_doc)

    all_stresses = []
    for stress in stress_terms:
        stress_doc = {}
        stress_doc['name'] = stress
        stress_doc['description'] = 'description'
        stress_doc['children'] = []
        all_stresses.append(stress_doc)
    sunflare['children'][0]['children'] = all_stresses

    stresses_sunflare = sunflare['children'][0]['children']
    for n, stress in enumerate(stresses_sunflare):
        name = stress['name']
        for article in articles_doc:
            article_stresses = article['stress']
            if name in article_stresses:
                if len(article['species']) != 0:
                    stress_species = stresses_sunflare[n]['children']
                    article_species = article['species']
                    all_article_species = [x['name'] for x in article_species]
                    for s, species in enumerate(all_article_species):
                        stress_species_list = [x['name'] for x in stress_species]
                        if species not in stress_species_list:
                            species_doc = {}
                            species_doc['name'] = species
                            species_doc['description'] = 'description'
                            species_doc['children'] = []
                            stress_species.append(species_doc)
                        else:
                            species_index = stress_species_list.index(species)
                            species_doc = stress_species[species_index]

                        if len(article_species[s]['genes']) != 0:
                            article_genes = article_species[s]['genes']
                            all_article_genes = [x['name'] for x in article_genes]
                            species_genes = species_doc['children']
                            species_genes_list = [x['name'] for x in species_genes]
                            for g, gene in enumerate(all_article_genes):
                                if gene not in species_genes_list:
                                    genes_doc = {}
                                    genes_doc['name'] = gene
                                    genes_doc['description'] = 'description'
                                    genes_doc['children'] = []
                                    species_genes.append(genes_doc)
                                else:
                                    gene_index = species_genes_list.index(gene)
                                    genes_doc = species_genes[gene_index]

                                if len(article_genes[g]['orthologs']) != 0:
                                    article_orthologs = article_genes[g]['orthologs']
                                    orthologs = [x for x in article_orthologs]
                                    gene_orthologs = genes_doc['children']
                                    gene_orthologs_list = [x['name'] for x in gene_orthologs]
                                    for ortholog in orthologs:
                                        if ortholog not in gene_orthologs_list:
                                            ortholog_doc = {}
                                            ortholog_doc['name'] = ortholog
                                            ortholog_doc['description'] = article_orthologs.get(ortholog)
                                            gene_orthologs.append(ortholog_doc)

    sunflare = json.loads(json.dumps(sunflare))
    print(sunflare)

    return sunflare

def construct_species_sunflare(articles_doc):
    species_sunflare = {}

    return species_sunflare
import requests

#Function for translating gene names to eggnog id's (via uniprot idmapper)
def species_identifier():
    #Defining the api URL
    uni_url = 'http://www.uniprot.org/uploadlists/'
    #Loading the gene file, should be replaced by JSON logic
    gene_file = open("all_genes.txt", "r")
    gene_lines = gene_file.read().splitlines()
    #Loading the all plants file which contains all (by uniprot) known abbrevations
    #for plants.
    species_file = open("all_plants.txt")
    species_lines = species_file.read().splitlines()




    counter =0
    #Creates a file to save the aquired data, should be replaced by JSON logic
    feest = open('herrie.txt', 'a')

    #Loops over the list of genes and requests uniprot to translate the genename to uniprot id's

    for i in gene_lines:
        counter += 1
        print(counter)
        #Defining parameters for the uniprot api
        payload = {
        'from': 'GENENAME',
        'to': 'ID',
        'format': 'list',
        'query': i
        }
        uniprot_id_request = requests.get(uni_url, params= payload)
        text1 = uniprot_id_request.text
        textsplit = text1.split()
        #check is used to check if a result needs to be saved or not.
        check = True
        #Loops over the list of uniprot id's and checks if it is in the list of plants
        #if it is in the list of plants it wil request uniprot to translate the uniprot id to an eggnog id and save this result.
        #It will only save the first result which is a plant and has a eggnog id.

        for x in textsplit:
            org = x.split("_")[1]

            if org in species_lines and check == True:
                print(x)
                #Defining parameters for the uniprot api
                payload_to_eggnog = {
                'from': 'ID',
                'to': 'EGGNOG_ID',
                'format': 'list',
                'query': x
                }
                #Uses the predefined parameters to request uniprot to translate an uniprot id to an eggnog id
                eggnog_id_request = requests.get(uni_url, params = payload_to_eggnog)

                #Builds a list based on the uniprot api results
                eggnog_id_text = eggnog_id_request.text
                eggnog_id_list = eggnog_id_text.split()

                #Checks if the list with eggnog id's isn't empty.
                if eggnog_id_list:
                    #writes the results to a file, should be replaced by JSON logic
                    feest.write('hier moet pubmed id herrie' + '\t' + i + '\t' + x + '\t' +eggnog_id_list[0] +'\n')
                    #makes sure only 1 eggnog id is saved per genename. 
                    check = False



def main():
    species_identifier()

main()

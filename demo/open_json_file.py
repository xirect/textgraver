import simplejson as json

def main():
    file = open('demo.json', 'r')
    graaf = file.read()

    graaf = json.loads(graaf)
    print(graaf)

main()
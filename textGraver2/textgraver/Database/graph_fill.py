
import subprocess

def fill_graph_files():


    subprocess.call("mongoexport --db TextGraver2 -c sunburst -o sunburst.json --jsonArray", shell=True)





def main():
    fill_graph_files()


main()

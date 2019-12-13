from datetime import datetime
from elasticsearch import Elasticsearch
import os

es = Elasticsearch()
os.system('gs -sDEVICE=txtwrite -o TextFiles/outputPy.txt Files/18-2019.pdf')

with open ("TextFiles/outputPy.txt", "r") as myfile:
    myData=myfile.readlines()

es.index(index="my-index", doc_type="test-type", id=44, body={"any": "data", "info": myData})
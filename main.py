from whoosh.analysis import StemmingAnalyzer, NgramFilter, StandardAnalyzer, NgramTokenizer
from whoosh.index import create_in, open_dir
from whoosh.fields import *
import os, os.path
import csv

from whoosh.qparser import QueryParser
my_analyzer = StandardAnalyzer()

schema = Schema(title=TEXT(analyzer=my_analyzer,stored=True), path=ID(stored=True), content=NGRAMWORDS(minsize=0,maxsize=4, stored=True))
#schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
ix = create_in("indexdir", schema)
writer = ix.writer()


with open('dataset/Reviews.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 100:
            break
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            writer.add_document(title=row[8], path=row[0], content=row[9])
            line_count += 1
    print(f'Processed {line_count} lines.')
    writer.commit()



from whoosh.index import create_in, open_dir
from whoosh.fields import *
import os, os.path
import csv

from whoosh.qparser import QueryParser

# schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))
# if not os.path.exists("indexdir"):
#     os.mkdir("indexdir")
# ix = create_in("indexdir", schema)
# writer = ix.writer()
#
#
#
# with open('dataset/Reviews.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count > 100:
#             break
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             writer.add_document(title=row[8], path=row[0], content=row[9])
#             line_count += 1
#     print(f'Processed {line_count} lines.')
#     writer.commit()

#Search in documents
ix = open_dir("indexdir")
searcher = ix.searcher()
parser = QueryParser("content", ix.schema)
print(ix.schema)
query =parser.parse(u"good")
results = searcher.search(query)

for res in results:
    print(res["content"])

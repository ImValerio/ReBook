from server.utils_fn import calculateSentimentNltk, calculateSentiment, removeStopWords
import csv
import os.path
from whoosh.analysis import StemmingAnalyzer, NgramFilter, StandardAnalyzer, NgramTokenizer
from whoosh.index import create_in
from whoosh.fields import TEXT, ID, NUMERIC, Schema
from decimal import Decimal
from decimal import *


my_analyzer = StandardAnalyzer()

schema = Schema(
    book_title=TEXT(analyzer=my_analyzer, stored=True),
    review_title=TEXT(analyzer=my_analyzer, stored=True),
    path=ID(stored=True, sortable=True),
    content=TEXT(analyzer=my_analyzer, stored=True, sortable=True),
    review_score=NUMERIC(stored=True),
    sentiment=NUMERIC(int, decimal_places=4, stored=True, sortable=True)
)
# schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
ix = create_in("indexdir", schema)
writer = ix.writer()


with open('dataset/Books_rating.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 5000:
            break
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            filtred_content = removeStopWords(row[9])
            sentiment = round(
                Decimal(calculateSentiment(row[9])), 4)
            # sentiment = Decimal(calculateSentiment(filtred_content))
            print(line_count, sentiment)
            writer.add_document(
                book_title=row[1], review_title=row[8], review_score=float(row[6]), path=row[0], content=row[9], sentiment=sentiment)
            line_count += 1
    print(f'Processed {line_count} lines.')
    writer.commit()

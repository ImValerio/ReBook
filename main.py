from whoosh.analysis import StemmingAnalyzer, NgramFilter, StandardAnalyzer, NgramTokenizer
from whoosh.index import create_in
from whoosh.fields import *
from decimal import Decimal
import os.path
import csv
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from torch.nn import functional as F

from whoosh.qparser import QueryParser
my_analyzer = StandardAnalyzer()

schema = Schema(
    title=TEXT(analyzer=my_analyzer, stored=True),
    path=ID(stored=True,sortable=True),
    content=TEXT(analyzer=my_analyzer, stored=True),
    review_score=NUMERIC(stored=True),
    sentiment=NUMERIC(int, decimal_places=4, stored=True, sortable=True)
)
#schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
ix = create_in("indexdir", schema)
writer = ix.writer()


tokenizer = AutoTokenizer.from_pretrained(
    "juliensimon/reviews-sentiment-analysis")
model = AutoModelForSequenceClassification.from_pretrained(
    "juliensimon/reviews-sentiment-analysis")


def calculateSentiment(review):
    inputs = tokenizer(review, return_tensors="pt",
                       truncation=True)

    logits = model(**inputs).logits
    softmax = F.softmax(logits, dim=1)
    return round(softmax[0][1].item(),4)


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
            sentiment = Decimal(calculateSentiment(row[9]))
            writer.add_document(
                title=row[8], review_score=row[6], path=row[0], content=row[9], sentiment=sentiment)
            line_count += 1
    print(f'Processed {line_count} lines.')
    writer.commit()

import math

from tkinter.tix import TEXT
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from whoosh import scoring
from whoosh.analysis import NgramTokenizer, StandardAnalyzer, NgramFilter, RegexTokenizer
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.query import *
from models.BM25F import BM25F
from models.CustomWeight import CustomWeight
from whoosh.scoring import WeightScorer
from utils_fn import calculateSentimentNltk

app = FastAPI()


def max_matcher():
    return 100000


class SearchText(BaseModel):
    text: Union[str, None] = None
    mode: Union[str, None] = None
    page: Union[int, None] = 1


def pos_sentiment_fn(searcher, fieldname, text, matcher):

    docnum = matcher.id()
    colreader = searcher.reader().column_reader("sentiment")
    sentiment = float(colreader[docnum])
    print("SENTIMENT: ", sentiment)

    return sentiment


@ app.post("/search")
def read_item(search: SearchText):

    ix = open_dir("../indexdir")

    # pos_weighting = scoring.FunctionWeighting(pos_score_fn)
    pos_weighting = CustomWeight()
    # k1: importanza frequenza di un termine; b: importanza lunghezza del documento
    if search.mode == "CONTENT_TEXT":
        pos_weighting = BM25F(B=0.75, content_B=1.0, K1=1.5)

    elif search.mode == "CONTENT_SENTIMENT":
        pos_weighting = CustomWeight(pos_sentiment_fn)

    from whoosh import query
    searcher = ix.searcher(weighting=pos_weighting)
    parser = MultifieldParser(["review_title", "content"],
                              ix.schema, termclass=query.Variations)
    query = parser.parse(search.text)

    results = searcher.search_page(query, search.page)

    dcg = 0

    results_score = [result.score for result in results]

    print(results_score)

    def normalizeBetweenZeroThree(res):
        start = 0
        end = 3
        width = end - start
        return (res - min(results_score))/((max(results_score)+1) - min(results_score)) * width + start

    results_score_norm = [round(normalizeBetweenZeroThree(res))
                          for res in results_score]

    print(results_score_norm)
    for i, rel in enumerate(results_score_norm):
        if i == 0:
            dcg += rel
        else:
            dcg += (rel / math.log2(i + 1))

    data = [{"id": res["path"], "book_title":res["book_title"], "review_title": res["review_title"],
             "content": res["content"], "length":len(res["content"]), "review_score":res["review_score"],  "score":res.score, "sentiment":res["sentiment"]} for res in results]

    ngf = NgramFilter(minsize=0, maxsize=3)
    rext = RegexTokenizer()
    stream = rext(search.text)

    corrected = searcher.correct_query(query, search.text)

    if not len(results):
        query = parser.parse(corrected.string)
        results = searcher.search(query)
        data = [{"id": res["path"], "title": res["title"],
                 "content": res["content"], "sentiment":res["sentiment"]} for res in results]

    ngrams = list(filter(None, [token.text for token in ngf(stream)]))
    query = Or([Term("content", ngram) for ngram in ngrams])

    results = searcher.search(query)

    return {"corrected": corrected.string, "results": data, "ngrams": list(results), "DCG": dcg}

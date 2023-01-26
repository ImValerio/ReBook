import math

from tkinter.tix import TEXT
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from whoosh import scoring, qparser
from whoosh.analysis import NgramTokenizer, StandardAnalyzer, NgramFilter, RegexTokenizer
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.query import *
from models.BM25F import BM25F
from models.CustomWeight import CustomWeight
from whoosh.scoring import WeightScorer
from utils_fn import calculateSentimentNltk, prioritizeTitle, normalizeBetweenZeroToN
from score_fn import sentiment_fn

app = FastAPI()


def max_matcher():
    return 100000


class SearchText(BaseModel):
    text: Union[str, None] = None
    mode: Union[str, None] = None
    page: Union[int, None] = 1


@ app.post("/search")
def read_item(search: SearchText):

    ix = open_dir("../indexdir")

    # pos_weighting = scoring.FunctionWeighting(pos_score_fn)
    pos_weighting = CustomWeight()
    # k1: importanza frequenza di un termine; b: importanza lunghezza del documento
    if search.mode == "CONTENT_TEXT":
        pos_weighting = BM25F(B=0.75, content_B=1.0, K1=1.5)

    elif search.mode == "CONTENT_SENTIMENT":
        pos_weighting = CustomWeight(sentiment_fn)
    # TODO: modificare il query language, mettere in and solo il titolo del libro
    from whoosh import query
    searcher = ix.searcher(weighting=pos_weighting)
    parser = MultifieldParser(["review_title", "content"],
                              ix.schema, termclass=query.Variations)
    query = prioritizeTitle(search.text, parser)
    print(query)
    results = searcher.search_page(query, search.page)
    dcg = []
    discounted_gain = []

    results_score = [result.score for result in results]

    print(results_score)

    results_score_norm = [round(normalizeBetweenZeroToN(res, results_score, 3))
                          for res in results_score]

    print("SCORE NORM: ", results_score_norm)

    for i, rel in enumerate(results_score_norm):
        if i == 0:
            discounted_gain.append(rel)
        else:
            discounted_gain.append(rel / math.log2(i + 1))

    discounted_gain_normalized = [round(normalizeBetweenZeroToN(res, discounted_gain, 1), 4)
                                  for res in discounted_gain]
    print("DG NORMALIZED: ", discounted_gain_normalized)
    for i, score in enumerate(discounted_gain_normalized):
        if i == 0:
            dcg.append(score)
        else:
            dcg.append(dcg[i-1] + score)

    data = [{"id": res["path"], "book_title":res["book_title"], "review_title": res["review_title"],
             "content": res["content"], "length":len(res["content"]), "review_score":res["review_score"],  "score":res.score, "sentiment":res["sentiment"]} for res in results]

    print("DCG: ", dcg)

    ngf = NgramFilter(minsize=0, maxsize=3)
    rext = RegexTokenizer()
    stream = rext(search.text)

    corrected = searcher.correct_query(query, search.text)

    if not len(results):
        query = parser.parse(corrected.string)
        results = searcher.search(query)
        data = [{"id": res["path"], "title": res["review_title"],
                 "content": res["content"], "sentiment":res["sentiment"]} for res in results]

    ngrams = list(filter(None, [token.text for token in ngf(stream)]))

    query_title = [Term("review_title", ngram_title) for ngram_title in ngrams]
    query_content = [Term("content", ngram) for ngram in ngrams]
    query = Or(query_title + query_content)
    results = searcher.search(query)

    return {"corrected": corrected.string, "results": data, "ngrams": list(results), "DCG": dcg}

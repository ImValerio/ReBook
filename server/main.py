from evalutation import get_discounted_gain, get_dcg
from tkinter.tix import TEXT
from typing import Union
from ngrams import get_ngrams
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
from utils_fn import calculateSentimentNltk, prioritizeTitle, normalizeBetweenZeroToN, get_review_obj
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
    results = searcher.search_page(query, search.page)

    results_score = [result.score for result in results]
    results_score_norm = [round(normalizeBetweenZeroToN(res, results_score, 3))
                          for res in results_score]
    discounted_gain_normalized = get_discounted_gain(results_score_norm)

    dcg = get_dcg(discounted_gain_normalized)

    results_ngrams = []
    data = get_review_obj(results)

    corrected = searcher.correct_query(query, search.text)
    # Se la query non restitusice alcun risultato => eseguo la query con la correzione della stringa utente
    if not len(results):
        query = parser.parse(corrected.string)
        results = searcher.search(query)
        data = get_review_obj(results)
        # Se la query 'corretta' non restituisce alcun risultato allora cerchiamo con i q-grams della stringa utente
        if not len(results):
            results_ngrams = get_ngrams(search.text, query, searcher)

    return {"corrected": corrected.string, "results": data, "ngrams": list(get_review_obj(results_ngrams)), "DCG": dcg}

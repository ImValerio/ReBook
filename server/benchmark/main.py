import sys
sys.path.append("../")

from whoosh.query import *
from whoosh.qparser import  MultifieldParser
from whoosh.index import open_dir
from utils_fn import  prioritizeTitle, normalizeBetweenZeroToN, get_review_obj
from ngrams import get_ngrams
from evalutation import get_discounted_gain, get_dcg
from models import BM25F
from whoosh.scoring import TF_IDF
from models import CustomWeight
from utils_fn import prioritizeTitle, normalizeBetweenZeroToN
from score_fn import sentiment_fn



def exec_query(text, mode):

    ix = open_dir("../../indexdir")

    # pos_weighting = scoring.FunctionWeighting(pos_score_fn)
    pos_weighting = CustomWeight()
    # k1: importanza frequenza di un termine; b: importanza lunghezza del documento
    if mode == "CONTENT_TEXT":
        pos_weighting = BM25F(B=0.75, content_B=1.0, K1=1.5)

    if mode == "CONTENT_TF_IDF":
        pos_weighting = TF_IDF()

    elif mode == "CONTENT_SENTIMENT":
        pos_weighting = CustomWeight(sentiment_fn)
    # TODO: modificare il query language, mettere in and solo il titolo del libro
    from whoosh import query
    searcher = ix.searcher(weighting=pos_weighting)
    parser = MultifieldParser(["review_title", "content"],
                              ix.schema, termclass=query.Variations)
    query = prioritizeTitle(text, parser)
    results = searcher.search_page(query, 1)

    results_score = [result.score for result in results]
    results_score_norm = [round(normalizeBetweenZeroToN(res, results_score, 3))
                          for res in results_score]
    discounted_gain_normalized = get_discounted_gain(results_score_norm)

    dcg = get_dcg(discounted_gain_normalized)

    results_ngrams = []
    data = get_review_obj(results)

    corrected = searcher.correct_query(query, text)
    # Se la query non restitusice alcun risultato => eseguo la query con la correzione della stringa utente
    if not len(results):
        query = parser.parse(corrected.string)
        results = searcher.search(query)
        results_score = [result.score for result in results]
        results_score_norm = [round(normalizeBetweenZeroToN(res, results_score, 3))
                          for res in results_score]
        discounted_gain_normalized = get_discounted_gain(results_score_norm)
        dcg = get_dcg(discounted_gain_normalized)
        data = get_review_obj(results)
        # Se la query 'corretta' non restituisce alcun risultato allora cerchiamo con i q-grams della stringa utente
        if not len(results):
            results_ngrams = get_ngrams(text, query, searcher)

    return {"corrected": corrected.string, "results": data, "ngrams": list(get_review_obj(results_ngrams)), "DCG": dcg}


queries = [
    "the best book in the world",
    "the most interesting book of this year",
    "a good cooking book",
    "The Scarletti Curse",
    "The Castle Attik",
    "adult book",
    "good reviews of |The Urban Primitive|",
    "adventure book for child",
    "horror book",
    "world war book"
]

modes = [
    "CONTENT_BM25",
    "CONTENT_TF_IDF",
    "CONTENT_SENTIMENT",
    "CONTENT_CUSTOM"
]

with open('benchmark.txt', 'w') as f:
    f.write("\n")
    f.write("N. QUERY (mode) \n")
    f.write("   DCG:[...] \n\n")
    for i,query in enumerate(queries):
        for mode in modes:
            result = exec_query(query, mode)
            f.write(str(i+1)+". "+query+" ("+mode+")\n")
            f.write("   "+str(result["DCG"])+"\n")
        f.write("\n")
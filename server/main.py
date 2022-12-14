from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from whoosh import scoring
from whoosh.analysis import NgramTokenizer, StandardAnalyzer, NgramFilter, RegexTokenizer
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import *

app = FastAPI()


class SearchText(BaseModel):
    text: Union[str, None] = None


def pos_score_fn(searcher, fieldname, text, matcher):
    poses = matcher.value_as("positions")
    print([field for field in searcher.all_stored_fields()])
    return 1.0 / (poses[0] + 1)


@ app.post("/search")
def read_item(search: SearchText):
    ix = open_dir("../indexdir")
    # k1: importanza frequenza di un termine; b: importanza lunghezza del documento
    # scoring.BM25F(B=-10.0, content_B=1.0, K1=1)

    pos_weighting = scoring.FunctionWeighting(pos_score_fn)
    from whoosh import query
    searcher = ix.searcher(weighting=pos_weighting)
    parser = QueryParser("content", ix.schema, termclass=query.Variations)
    query = parser.parse(search.text)

    results = searcher.search(query)

    data = [{"id": res["path"], "title": res["title"],
             "content": res["content"], "sentiment":res["sentiment"], "length":len(res["content"])} for res in results]

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
    print(ngrams)
    query = Or([Term("content", ngram) for ngram in ngrams])

    results = searcher.search(query)

    return {"corrected": corrected.string, "results": data, "ngrams": list(results)}

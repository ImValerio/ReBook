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
# def custom_scoring(searcher, fieldname, text, matcher):
#     bm25 = scoring.BM25F().scorer(searcher, fieldname, text).score(matcher)
#     return  bm25 + score

@app.post("/search")
def read_item(search: SearchText):
    ix = open_dir("../indexdir")
    scoring.BM25F(B=0.75, content_B=1.0, K1=1.5)
    # scoring.FunctionWeighting()

    from whoosh import query
    searcher = ix.searcher()
    parser = QueryParser("content", ix.schema, termclass=query.Variations)
    query = parser.parse(search.text)

    results = searcher.search(query)
    data = [{"id": res["path"], "review_score":res["review_score"], "title": res["title"],
             "content": res["content"]} for res in results]

    ngf = NgramFilter(minsize=0, maxsize=3)
    rext = RegexTokenizer()
    stream = rext(search.text)

    corrected = searcher.correct_query(query, search.text)
    if not len(results):
        query = parser.parse(corrected.string)
        results = searcher.search(query)

        data = [{"id": res["path"], "review_score":res["review_score"], "title": res["title"],
                 "content": res["content"], "sort": (res.score + float(res["review_score"]))} for res in results]

        data.sort(key=lambda company: company["sort"],reverse=True)

    ngrams = list(filter(None, [token.text for token in ngf(stream)]))
    print(ngrams)
    query = Or([Term("content", ngram) for ngram in ngrams])

    results = searcher.search(query)

    return {"corrected": corrected.string, "results": data, "ngrams": list(results)}

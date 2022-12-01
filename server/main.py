from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

app = FastAPI()


class SearchText(BaseModel):
    text: Union[str, None] = None


@app.post("/search")
def read_item(search: SearchText):
    ix = open_dir("../indexdir")

    searcher = ix.searcher()
    parser = QueryParser("content", ix.schema)
    query = parser.parse(search.text)

    results = searcher.search(query)

    data = [{"id": res["path"], "title": res["title"], "content": res["content"]} for res in results]

    return {"results": data}

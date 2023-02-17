from whoosh.analysis import NgramFilter, RegexTokenizer
from whoosh.query import Term, Or


def get_ngrams(text, query, searcher,page):
    ngf = NgramFilter(minsize=0, maxsize=3)
    rext = RegexTokenizer()
    stream = rext(text)

    ngrams = list(filter(None, [token.text for token in ngf(stream)]))

    query_title = [Term("review_title", ngram_title)
                   for ngram_title in ngrams]
    query_content = [Term("content", ngram) for ngram in ngrams]
    query = Or(query_title + query_content)

    results = searcher.search_page(query, page)
    return results

from math import log

from whoosh.compat import iteritems
from whoosh.scoring import WeightingModel, WeightLengthScorer, WeightScorer
from utils_fn import calculateSentimentNltk
from whoosh.scoring import BaseScorer
from score_fn import pos_sentiment_fn


def max_tmp():
    return 10


class CustomWeight(WeightingModel):
    def __init__(self, fn=pos_sentiment_fn):
        self.fn = fn
        self.max_quality = 10

    def scorer(self, searcher, fieldname, text, qf=1):
        return self.FunctionScorer(self.fn, searcher, fieldname, text, qf=qf)

    class FunctionScorer(BaseScorer):
        def __init__(self, fn, searcher, fieldname, text, qf=1, max_quality=max_tmp):
            self.fn = fn
            self.searcher = searcher
            self.fieldname = fieldname
            self.text = text
            self.qf = qf
            self.max_quality = max_quality

        def score(self, matcher):
            return self.fn(self.searcher, self.fieldname, self.text, matcher)

        def max_quality(self):
            return 10

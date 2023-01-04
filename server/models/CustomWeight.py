from math import log

from whoosh.compat import iteritems
from whoosh.scoring import WeightingModel, WeightLengthScorer, WeightScorer
from utils_fn import calculateSentimentNltk
from whoosh.scoring import BaseScorer


def score_fn(searcher, fieldname, text, matcher):
    poses = matcher.value_as("positions")

    print(fieldname, poses)

    docnum = matcher.id()
    colreader = searcher.reader().column_reader("sentiment")
    sentiment = float(colreader[docnum])

    position_score = 1/(poses[0] + 1)
    percentage_score = position_score * sentiment

    score = round(position_score + percentage_score, 5)

    print(score)
    return score


def max_tmp():
    return 10


class CustomWeight(WeightingModel):
    def __init__(self, fn=score_fn):
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

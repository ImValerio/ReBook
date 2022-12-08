from whoosh.scoring import WeightingModel, BM25F


class MyWeightingModel(WeightingModel):

    def scorer(self, searcher, fieldname, score):
        # calculate the length of the text

        # create the scorer object using BM25F
        scorer = BM25F(searcher, fieldname)

        # override the score() method to return a custom score
        # that takes into account the length of the text
        def score(self):
            # get the original BM25F score
            original_score = scorer.score()

            # return a new score that is weighted by the length of the text
            return original_score * score

        return score
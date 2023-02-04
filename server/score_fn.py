
def sentiment_fn(searcher, fieldname, text, matcher):
    docnum = matcher.id()
    colreader = searcher.reader().column_reader("sentiment")
    sentiment = float(colreader[docnum])

    return sentiment


def pos_sentiment_fn(searcher, fieldname, text, matcher):
    poses = matcher.value_as("positions")

    docnum = matcher.id()
    colreader = searcher.reader().column_reader("sentiment")
    sentiment = float(colreader[docnum])

    position_score = 1/(poses[0] + 1)
    percentage_score = position_score * sentiment

    score = round(position_score + percentage_score, 5)

    return score

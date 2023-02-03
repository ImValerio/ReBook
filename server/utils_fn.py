import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn import functional as F
from whoosh.query import And, Or, Variations, Term

# tokenizer = AutoTokenizer.from_pretrained(
#    "review-sentiment-analysis", local_files_only=True)
tokenizer = AutoTokenizer.from_pretrained(
    "juliensimon-reviews-sentiment-analysis", local_files_only=True)
# model = AutoModelForSequenceClassification.from_pretrained(
#    "review-sentiment-analysis/pytorch_model.bin", local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(
    "juliensimon-reviews-sentiment-analysis", local_files_only=True)


def removeStopWords(text):
    newText = ""
    tokenizer = RegexpTokenizer(r'\w+')
    # tokens = nltk.word_tokenize(text)
    tokens = tokenizer.tokenize(text)
    for t in tokens:
        if not t in stopwords.words('english'):
            newText = newText + " "+t

    return newText


def calculateSentiment(review):
    inputs = tokenizer(review, return_tensors="pt",
                       truncation=True)
    logits = model(**inputs).logits
    softmax = F.softmax(logits, dim=1)
    return round(softmax[0][1].item(), 4)


def calculateSentimentNltk(review):
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sid = SentimentIntensityAnalyzer()
    # nltk.data.path.append('vader_lexicon')
    sentiment_score = round(float(sid.polarity_scores(review)['pos']), 4)
    return sentiment_score


def normalizeBetweenZeroAndOne(res):
    start = 0
    end = 1
    width = end - start
    return (res - 0)/((1+1) - 0) * width + start


def haveTitle(text):
    return "|" in text


def prioritizeTitle(text, parser):
    if haveTitle(text):

        title_split = text.split("|")
        book_title = removeStopWords(title_split[1].lower()).strip().split(" ")
        # query_book_title = [And([Or([Term('review_title', word_title), Term(
        # 'content', word_title)]) for word_title in book_title])]
        query_book_title = [And([Term('book_title', word_title)
                                for word_title in book_title])]

        title_split.pop(1)
        text_without_title = removeStopWords(
            " ".join(title_split)).strip().split(" ")
        final_query = Or(query_book_title + [Or([Variations('review_title', word_title), Variations(
            'content', word_title)]) for word_title in text_without_title])

        return final_query

    return parser.parse(text)


def normalizeBetweenZeroToN(res, results_score, end):
    start = 0
    width = end - start
    return (res - min(results_score))/((max(results_score)+1) - min(results_score)) * width + start


def get_review_obj(review_array):
    return [{"id": res["path"], "book_title":res["book_title"], "review_title": res["review_title"],
             "content": res["content"], "length":len(res["content"]), "review_score":res["review_score"],  "score":res.score, "sentiment":res["sentiment"]} for res in review_array]

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn import functional as F

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


def prioritizeTitle(text):
    if haveTitle(text) and text.index("|") > 3:

        title_split = text.split("|")
        title_split.insert(0, title_split[1])
        title_split.pop(2)

        res = " ".join(title_split)

        return res

    return text

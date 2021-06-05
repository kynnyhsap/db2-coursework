from textblob import TextBlob


def get_polarity(text: str):
    return TextBlob(text).sentiment.polarity


def get_subjectivity(text: str):
    return TextBlob(text).sentiment.subjectivity


def get_score_label(score):
    if score > 0:
        return 'positive'

    if score < 0:
        return 'negative'

    return 'neutral'

import re
import preprocessor as tweet_preprocessor


def clean_tweet(tweet: str):
    return tweet_preprocessor.clean(tweet)


def tokenize_tweet(tweet: str):
    return tweet_preprocessor.tokenize(tweet)


def remove_retweet_prefix(tweet: str):
    return re.sub(r'RT : ', '', tweet)  # TODO: add @mentions to this regex

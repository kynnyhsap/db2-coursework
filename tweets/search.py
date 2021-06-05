from tweets.api import TweeterClient


def recent_tweets_search(query='', limit=100):
    tweets = TweeterClient().search(query, limit=limit)

    return tweets

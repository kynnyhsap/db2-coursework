import os
import tweepy as tw
from dotenv import load_dotenv

load_dotenv()


CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']


class TweeterClient:
    def __init__(self):
        try:
            auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

            self.api = tw.API(auth, wait_on_rate_limit=True)
        except tw.auth.TweepError as e:
            print("Error: Twitter Authentication Failed", e)

    def search(self, search, limit=5):
        # TODO: multi page search
        try:
            statuses = self.api.search(search, count=limit, lang="en", tweet_mode='extended')

            return list([{
                'id': tweet.id,
                'text': tweet.full_text,
            } for tweet in statuses])
        except tw.TweepError as e:
            print("Error : " + str(e))
            return []

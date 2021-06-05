import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_REPLICA_SET = os.environ['MONGO_REPLICA_SET']
MONGO_PORT = int(os.environ['MONGO_PORT'])


class TweetsDB:
    def __init__(self):
        client = MongoClient('localhost', MONGO_PORT, replicaset=MONGO_REPLICA_SET)

        self.db = client['test']

    def find_tweet_by_id(self, id):
        return self.db['tweets'].find_one({'id': id})

    def find_tweets_by_search(self, search_query):
        return [t for t in self.db['tweets'].find({'search_query': search_query})]

    def save_tweets(self, tweets_df):
        documents = tweets_df.to_dict('records')

        # filtered_documents = list(filter(self.find_tweet_by_id, [doc['id'] for doc in documents]))
        # print(filtered_documents)

        total_saved = 0

        for doc in documents:
            tweet = self.find_tweet_by_id(doc['id'])
            if tweet is not None:
                continue
            self.db['tweets'].insert_one(doc)
            total_saved += 1

        return total_saved

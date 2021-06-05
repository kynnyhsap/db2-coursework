import click
from tweets.db import TweetsDB
from tweets.processing import clean_tweet
from tweets.search import recent_tweets_search
from tweets.sentiment import get_polarity, get_subjectivity, get_score_label
from tweets.reports import score_piechart, build_wordcloud, polarity_histogram
import pandas as pd
from datetime import datetime
from pathlib import Path


@click.command()
@click.option('--limit', default=100, help='Max number of tweets to search.')
@click.argument('search-query')
def demo_search(limit: int = 100, search_query: str = ''):
    tweets = recent_tweets_search(search_query, limit)

    for i in range(limit):
        if i >= len(tweets):
            break

        tweet = tweets[i]
        original_text = tweet['text']

        click.secho(f"\n{i + 1} ID:[{tweet['id']}]", bold=True)
        click.secho(f"  - {original_text}", fg='blue')


@click.command()
@click.option('--limit', default=100, help='Max number of tweets to search.')
@click.option('--search-query', default='#top', help='Search query for tweets.')
def generate_dataset(limit: int = 100, search_query: str = ''):
    # retrieving tweets data
    tweets = recent_tweets_search(search_query, limit)

    # creating dataset
    tweets_df = pd.DataFrame({
        'id': [tweet['id'] for tweet in tweets],
        'search_query': search_query,
        'original_text': [tweet['text'] for tweet in tweets],
    })

    # dataset preprocessing
    tweets_df['cleaned_text'] = tweets_df['original_text'].apply(clean_tweet)

    # sentiment analysis
    tweets_df['polarity'] = tweets_df['cleaned_text'].apply(get_polarity)
    tweets_df['subjectivity'] = tweets_df['cleaned_text'].apply(get_subjectivity)
    tweets_df['score'] = tweets_df['polarity'].apply(get_score_label)

    db = TweetsDB()
    total_saved = db.save_tweets(tweets_df)

    print(tweets_df)
    print(f'Successfully saved {total_saved} tweets in DB.')


@click.command()
@click.option('--topic', help='Search query for tweets.')
def visual_report(topic: str = ''):
    db = TweetsDB()

    tweets = db.find_tweets_by_search(topic)

    if len(tweets) > 0:
        print(f'Found {len(tweets)} tweets for topic "{topic}".')
    else:
        print(f'Tweets for topic "{topic}" not found in database.')
        return

    # TODO: documents to pandas.DataFrame
    # creating dataset
    tweets_df = pd.DataFrame(tweets)

    # create reports folder
    report_folder = f'./reports/{str(datetime.utcnow())}'
    Path(report_folder).mkdir(parents=True, exist_ok=True)

    # create score barchart
    score_piechart(tweets_df, field='score', title=topic, filename=report_folder + '/score-piechart.png')
    # create polarity histogram
    polarity_histogram(tweets_df, field='polarity', title=topic, filename=report_folder + '/polarity-histogram.png')
    # create word cloud
    all_tweets_text = ' '.join([text for text in tweets_df['cleaned_text']])
    build_wordcloud(all_tweets_text, filename=report_folder + '/tweets-wordcloud.png')

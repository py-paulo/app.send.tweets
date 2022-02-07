import os

import requests
import boto3
import click

from rich import print
from dotenv import dotenv_values

from sqstw.tw import search_tweets
from sqstw.utils import tweet_in_message_attributes_sqs
from sqstw.sqs import sqs_send_message

config = {
    **dotenv_values(".env"),
    **os.environ,  # override loaded values with environment variables
}


def __sqs_send_message(sqs, queue_url, tw, text):
    return sqs_send_message(sqs, queue_url, tweet_in_message_attributes_sqs(tw), text)


@click.group()
def cli():
    pass


@cli.command('tw-to-sqs')
@click.option('--queue-url', default=config.get('SQS_QUEUE_URL'), help='SQS queue url.')
@click.option('--twitter-token', default=config.get('TWITTER_BEARER_TOKEN'), help='Bearer token Twitter.')
@click.option('--one-twitter', default=False, help='Send only one Tweet.')
def cli_sqstw(queue_url, twitter_token, one_twitter):
    sqs = boto3.client('sqs')
    tw_data = search_tweets(twitter_token).get('data')

    if not one_twitter:
        for tweet in tw_data:
            tw = tweet_in_message_attributes_sqs(tweet)
            message_id = sqs_send_message(sqs, queue_url, tw, tweet['text'])
            print(message_id)
    else:
        tweet = tw_data[0]
        tw = tweet_in_message_attributes_sqs(tweet)
        message_id = sqs_send_message(sqs, queue_url, tw, tweet['text'])
        print(message_id)


@cli.command('tw-to-lambda')
@click.option('--url', default=config.get('API_GATEWAY_URL'), help='Api Gateway URL.')
@click.option('--twitter-token', default=config.get('TWITTER_BEARER_TOKEN'), help='Bearer token Twitter.')
@click.option('--one-twitter/--all-twitters', default=False, help='Send only one Tweet.')
def cli_tw_to_lambda(url, twitter_token, one_twitter):
    tw_data = search_tweets(twitter_token).get('data')
    if not one_twitter:
        for tweet in tw_data:
            req = requests.post(url, json=tweet, headers={'Content-Type': 'application/json'})
            print(req.json())
    else:
        req = requests.post(url, json=tw_data[0])
        print(req.json())


if __name__ == '__main__':
    cli()

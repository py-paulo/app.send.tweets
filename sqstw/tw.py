import requests

from .constants import TWITTER_GET_RECENTS_TWEETS


def search_tweets(bearer_token: str):
    """
    {
    'data': [
        {
            'id': '1489037222208753673',
            'entities': {
                'annotations': [{'start': 48, 'end': 53, 'probability': 0.579, 'type': 'Person', 'normalized_text': 'Hoodad'}],
                'mentions': [{'start': 3, 'end': 18, 'username': 'TerrierWheaten', 'id': '1471934231177838597'}]
            },
            'text': 'RT @TerrierWheaten: I call this my “Sun Beard!” Hoodad says I’m definitely gonna be on the receiving end of a big brushing shortly…of cours…',
            'created_at': '2022-02-03T00:45:13.000Z'
        },
        ...
    ], ...
    }
    """
    req = requests.get(
        TWITTER_GET_RECENTS_TWEETS,
        headers={
            'Authorization': f'Bearer {bearer_token}'
            }
        )

    return req.json()

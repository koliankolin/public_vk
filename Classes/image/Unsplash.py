import requests
import random
import mem_const
import constants

class Unsplash:
    def __init__(self):
        self.api_url = 'https://api.unsplash.com/search/photos'

    def loadImageUrl(self):
        params = {
            'query': random.choice(mem_const.QUERIES_SEARCH),
            'orientation': 'squarish',
            'client_id': constants.UPSLASH_CLIENT_ID,
        }
        return random.choice(requests.get(self.api_url, params=params).json()['results'])['urls']['regular']



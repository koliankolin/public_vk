import requests
import random
import mem_const
import constants

class Unsplash:
    def __init__(self):
        self.api_url = 'https://api.unsplash.com/search/photos'

    def loadImageUrl(self):
        # params = {
        #     'query': 'meme',#random.choice(mem_const.QUERIES_SEARCH),
        #     'orientation': 'squarish',
        #     'client_id': constants.UPSLASH_CLIENT_ID,
        #     'order_by': 'latest',
        #     'per_page': 10,
        #     'page': 1,
        # }
        # return random.choice(requests.get(self.api_url, params=params).json()['results'])['urls']['regular']
        return 'https://source.unsplash.com/random/600x500/'

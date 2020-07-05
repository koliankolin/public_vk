import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import constants


class NewsLoader:
    def __init__(self, source, img_count):
        self.img_count = img_count
        self.ua = UserAgent()

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, source):
        if source not in ['upslash']:
            self.__source = 'upslash'
        else:
            self.__source = source

    def _getHeaders(self):
        return {
            'User-Agent': self.ua.chrome
        }



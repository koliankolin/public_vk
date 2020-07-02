import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import constants


class NewsLoader:
    def __init__(self, source, news_count):
        self.source = source
        self.news_count = news_count
        self.ua = UserAgent()
        self.mainBs = BeautifulSoup(self._getMainNewsPage(), 'lxml')

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, source):
        if source not in ['mirror', 'sky']:
            self.__source = 'mirror'
        else:
            self.__source = source

    def _getHeaders(self):
        return {
            'User-Agent': self.ua.chrome
        }

    def _getMainNewsPage(self):
        source_url = constants.SOURCES_URLS[self.source]['url']
        return requests.get(source_url, headers=self._getHeaders()).text

    def _getTeasersFromMainPage(self):
        teaser_cls = constants.SOURCES_URLS[self.source]['teaser_cls']
        return self.mainBs.findAll('div', {'class': teaser_cls})[:self.news_count]

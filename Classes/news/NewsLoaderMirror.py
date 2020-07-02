import requests
from bs4 import BeautifulSoup
import time
from Mappers.News import News
from Classes.news.NewsLoader import NewsLoader
from googletrans import Translator
from tqdm import tqdm


class NewsLoaderMirror(NewsLoader):
    def getNewsMappers(self):
        tr = Translator()
        result = []
        print('Load News...')
        for teaser in tqdm(self._getTeasersFromMainPage()):
            a = teaser.find('figure').find('a', href=True)
            img = a.find('img')['data-src']
            if 'https://' not in img:
                continue
            link_news = a['href']
            if '/sport/football/' not in link_news:
                continue
            text_teaser = a['aria-label']

            rs = requests.get(link_news, headers=self._getHeaders())
            soup = BeautifulSoup(rs.text, 'lxml')
            full_text = soup.find('p', {'class': 'sub-title'})
            if not full_text:
                continue
            full_text = full_text.contents[0]
            t = News(
                text_teaser,
                full_text,
                tr.translate(text_teaser, dest='ru', src='en').text,
                tr.translate(full_text, dest='ru', src='en').text,
                link_news,
                img,
                self.source,
            )
            result.append(t)
            time.sleep(10)

        return result


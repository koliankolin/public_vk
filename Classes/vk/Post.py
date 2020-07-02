import constants
from Classes.vk.Base import Base
from Classes.vk.Image import Image
from Classes.news.NewsLoaderMirror import NewsLoaderMirror
from tqdm import tqdm


class Post(Base):
    def __init__(self):
        super().__init__()
        self.news = NewsLoaderMirror('mirror', 2)

    def post(self, publish_date=None):
        for new in tqdm(self.news.getNewsMappers()[::-1]):
            try:
                self.api.method('wall.post', {
                    'owner_id': -constants.VK_GROUP_ID,
                    'from_group': 1,
                    'message': f'{new.teaser_en}\n\n{new.text_en}\n\n---------------------------------------\n\n{new.teaser_ru}\n\n{new.text_ru}\n\nИсточник:  {new.source.capitalize()}',
                    'attachments': Image(photo_link=new.img).loadPhoto(),
                    'publish_date': publish_date,
                    'signed': 0,
                })
            except:
                continue
        print('All posted')

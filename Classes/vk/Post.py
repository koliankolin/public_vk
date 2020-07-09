import constants
from Classes.vk.Base import Base
from Classes.vk.Image import ImageCls
from Classes.image.NewsLoaderMirror import NewsLoaderMirror
from tqdm import tqdm
import time

class Post(Base):
    def __init__(self):
        super().__init__()

    def post(self, publish_dates=()):
        for i, date in enumerate(publish_dates):
            # try:
            self.api.method('wall.post', {
                'owner_id': -constants.VK_GROUP_ID,
                'from_group': 1,
                # 'message': f'{new.teaser_en}\n\n{new.text_en}\n\n---------------------------------------\n\n{new.teaser_ru}\n\n{new.text_ru}\n\nИсточник:  {new.source.capitalize()}',
                'attachments': ImageCls().loadMem(),
                'publish_date': date,
                'signed': 0,
            })
            time.sleep(3)
        #     except:
        #         print('Something went wrong')
        #         exit(1)
        # print('All posted')

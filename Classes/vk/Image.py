import constants
from Classes.vk.Base import Base
import requests, os


class Image(Base):
    def __init__(self, photo_link):
        super().__init__()
        self.photo_link = photo_link

    def loadPhoto(self):
        _, ext = os.path.splitext(self.photo_link)
        img_data = requests.get(self.photo_link).content
        file_name = f'./img/sample{ext}'
        with open(file_name, 'wb') as handler:
            handler.write(img_data)
        photo = self.uploader.photo_wall(file_name, group_id=constants.VK_GROUP_ID)[0]
        return 'photo{owner_id}_{id}'.format(**photo)
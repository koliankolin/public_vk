from Classes.vk.Base import Base
import time
from fake_useragent import UserAgent
import requests

class Utils(Base):
    def __init__(self):
        super().__init__()

    def getFullNameById(self, ids=()):
        res = self.api.method('users.get', {
            'user_ids': ','.join([str(id_) for id_ in ids]),
        })
        time.sleep(0.4)
        return [f'{user["first_name"]} {user["last_name"]}' for user in res]

    def downloadPhotoByUrl(self, url, out_path):
        ua = UserAgent()
        headers = {
            'User-Agent': ua.chrome
        }
        img_data = requests.get(url, headers=headers).content
        with open(out_path, 'wb') as handler:
            handler.write(img_data)

        return out_path

    def downloadPhotoById(self, id_):
        res = self.api.method('users.get', {
            'user_ids': str(id_),
            'fields': 'photo_200',
        })[0]

        out_file = self.downloadPhotoByUrl(res['photo_200'], 'img/avatar.jpg')
        time.sleep(0.4)
        return out_file


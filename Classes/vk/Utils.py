from Classes.vk.Base import Base
import time
from fake_useragent import UserAgent
import requests
from datetime import datetime

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

    @staticmethod
    def checkIsSunday():
        return datetime.today().weekday() == 6

    def getWeekId(self):
        with open('week.id', 'r') as f:
            week_id = f.readline()
        if self.checkIsSunday():
            with open('week.id', 'w') as f:
                f.write(str(int(week_id) + 1))
        return week_id

    @staticmethod
    def plural_days(n):
        days = ['день', 'дня', 'дней']

        if n % 10 == 1 and n % 100 != 11:
            p = 0
        elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
            p = 1
        else:
            p = 2

        return str(n) + ' ' + days[p]

    @staticmethod
    def getWeekNamesRating():
        with open('week_rating.id', 'r') as f:
            names = f.readline().split(',')
            photos = f.readline().split(',')

        return names, photos

    @staticmethod
    def saveNamesAndPhotosWeek(names, photos):
        with open('week_rating.id', 'w') as f:
            f.write(','.join(names))
            f.write(','.join(photos))



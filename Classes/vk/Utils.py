from Classes.vk.Base import Base
import time

class Utils(Base):
    def __init__(self):
        super().__init__()

    def getFullNameById(self, ids=()):
        res = self.api.method('users.get', {
            'user_ids': ','.join([str(id_) for id_ in ids]),
        })
        time.sleep(0.4)
        return [f'{user["first_name"]} {user["last_name"]}' for user in res]

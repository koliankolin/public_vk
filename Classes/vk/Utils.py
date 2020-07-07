from Classes.vk.Base import Base


class Utils(Base):
    def __init__(self):
        super().__init__()

    def getFullNameById(self, id_):
        res = self.api.method('users.get', {
            'user_ids': id_,
        })[0]
        return f'{res["first_name"]} {res["last_name"]}'

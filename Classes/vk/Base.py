import constants
import vk_api
from vk_api import VkUpload


class Base:
    def __init__(self):
        session = vk_api.VkApi(app_id=constants.VK_APP_ID, login=constants.VK_LOGIN, password=constants.VK_PASSWORD, scope=constants.VK_SCOPE)
        session.auth()
        self.api = session
        self.uploader = VkUpload(session)

import requests
import constants


class ImageLoader:
    def __init__(self):
        # self.tokenService =

    def _getUploadLink(self):
        url = constants.VK_URL + 'photos.getWallUploadServer'
        res = requests
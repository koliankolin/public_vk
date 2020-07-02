import constants
from Classes.vk.BaseLoader import BaseLoader


class ImageLoader(BaseLoader):
    def __init__(self, photo_path):
        super().__init__()
        self.photo_path = photo_path

    def _getUploadLink(self):
        return self.api.photos.getWallUploadServer(group_id=constants.VK_GROUP_ID, v=constants.VK_VERSION)['upload_url']

    def loadPhoto(self):
        photo = self.uploader.photo_wall(self.photo_path, group_id=constants.VK_GROUP_ID)[0]
        photo = 'photo{owner_id}_{id}'.format(**photo)
        return self.api.method('wall.post', {
            'owner_id': -constants.VK_GROUP_ID,
            'from_group': 1,
            'message': 'test',
            'attachments': photo,
        })
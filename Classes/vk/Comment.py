from Classes.vk.Base import Base
import constants


class Comment(Base):
    def __init__(self, start_time, end_time):
        super().__init__()
        self.start_time = start_time
        self.end_time = end_time

    def _getPostIds(self):
        posts = self.api.method('newsfeed.get', {
            'filters': 'post',
            'start_time': self.start_time,
            'end_time': self.end_time,
            'source_ids': -constants.VK_GROUP_ID,
            'count': 100,
        })['items']
        return [post['post_id'] for post in posts]

    def getComments(self):
        postIds = self._getPostIds()
        for postId in postIds:
            comments = self.api.method('wall.getComments', {
                'owner_id': -constants.VK_GROUP_ID,
                'post_id': str(postId),
                'need_likes': 1,
                'count': 100,
            })['items'] # from_id, id, text


from Classes.vk.Base import Base
import constants
import time
import random
from datetime import datetime

class Comment(Base):
    def __init__(self, start_time, end_time):
        super().__init__()
        self.start_time = start_time
        self.end_time = end_time
        self.subscribers = self._getAllSubscribers()
        self.posts = self._getPosts()

    def _getPosts(self):
        return self.api.method('newsfeed.get', {
            'filters': 'post',
            'start_time': self.start_time,
            'end_time': self.end_time,
            'source_ids': -constants.VK_GROUP_ID,
            'count': 100,
        })['items']

    def _getPostIds(self):
        return [post['post_id'] for post in self.posts]

    def getComments(self):
        postIds = self._getPostIds()
        comments = []
        for postId in postIds:
            preparedComments = self._prepareComments(self.api.method('wall.getComments', {
                'owner_id': -constants.VK_GROUP_ID,
                'post_id': str(postId),
                'need_likes': 1,
                'count': 100,
            })['items'], postId) # from_id, id, text
            comments += preparedComments
        bestComment = self._getBestComment(comments)
        bestComment = bestComment if bestComment else random.choice(comments)
        leaderBoard = self._getLeaderBoard(comments)
        res = self.api.method('wall.post', {
            'owner_id': -constants.VK_GROUP_ID,
            'from_group': 1,
            'message': self._createMessage(bestComment, leaderBoard),
            # 'attachments': Image(photo_link=new.img).loadPhoto(),
            'signed': 0,
        })

        return res

    def _createMessage(self, bestComment, leaderBoard):
        frm = '%d.%m.%Y'
        date_start = datetime.utcfromtimestamp(self.start_time).strftime(frm)
        date_end = datetime.utcfromtimestamp(self.end_time).strftime(frm)
        return f"""Лучшие мамкины комментаторы недели ({date_start} - {date_end})
        
        Лучший комментарий:
        Награждается [https://vk.com/id{bestComment['from_id']}|id{bestComment['from_id']}] за комментарий 
        "{bestComment['text']}" к [https://vk.com/public196777471?w=wall-196777471_{bestComment['post_id']}|посту]
        Приз: {constants.BEST_COMMENT_PRIZE} р.
        
        Лидеры комментаторов:
        {self._leaderBoardToStr(leaderBoard)}
        """

    def _getLeaderBoard(self, comments):
        users = {}
        for comment in comments:
            users.setdefault(comment['from_id'], 0)
            users[comment['from_id']] += comment['likes_count']
        return sorted(users.items(), key=lambda item: item[1], reverse=True)[:3]

    @staticmethod
    def _leaderBoardToStr(leaderBoard):
        result = ''
        for (i, val), price in zip(enumerate(leaderBoard), constants.PRIZES):
            id_, likes = val
            result += f"{i + 1}. [https://vk.com/id{id_}|id{id_}] - {likes} likes. Приз: {price} р.\n"
        return result

    def _prepareComments(self, comments, post_id):
        result = []
        for comment in comments:
            if comment['from_id'] in self.subscribers:
                result.append({
                    'from_id': comment['from_id'],
                    'id': comment['id'],
                    'likes_count': self._getOurLikesByCommentId(comment['id']),
                    'text': comment['text'],
                    'post_id': post_id,
                })

        return result

    def _getOurLikesByCommentId(self, comment_id):
        page = 0
        limit = 1000
        result = []
        while True:
            offset = page * limit
            res = self.api.method('likes.getList', {
                'type': 'comment',
                'owner_id': -constants.VK_GROUP_ID,
                'item_id': comment_id,
                'count': 1000,
            })
            result += res['items']
            if res['count'] < offset + limit:
                break
            print(res['count'])
            page += 1
            time.sleep(0.4)

        return len(set(result).intersection(self.subscribers))

    @staticmethod
    def _getBestComment(comments, min_likes=constants.MIN_LIKES):
        bestComment = max(comments, key=lambda x: x['likes_count'])
        return bestComment if bestComment['likes_count'] > min_likes else None

    def _getAllSubscribers(self):
        page = 0
        limit = 1000
        result = []
        while True:
            offset = page * limit
            res = self.api.method('groups.getMembers', {
                'group_id': constants.VK_GROUP_ID,
                'offset': offset,
                'count': limit,
            })
            result += res['items']
            if res['count'] < offset + limit:
                break
            page += 1
            time.sleep(0.4)

        return set(result)


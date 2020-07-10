from Classes.vk.Base import Base
import constants
import time
import time
from datetime import datetime
from collections import Counter, OrderedDict
import os
from Classes.vk.Image import ImageCls
from Classes.vk.Utils import Utils


class Comment(Base):
    def __init__(self, start_time, end_time):
        super().__init__()
        self.start_time = start_time
        self.end_time = end_time
        self.subscribers = self._getAllSubscribers()
        self.posts = self._getPosts()
        self.fileStatsPostId = 'stats.id'
        self.utils = Utils()

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

    def getStats(self):
        postIds = self._getPostIds()
        comments = []
        counterPostLikes = Counter()
        counterCommentLikes = Counter()
        counterComments = Counter()
        counterReposts = Counter()
        for postId in postIds:
            counterPostLikes += self._getCounterUsersLikesByPostId(postId)
            commentsByPostId = self._getAllCommentsByPostId(postId)
            preparedComments = self._prepareComments(commentsByPostId, postId)
            counterCommentLikes += self._getTotalCounterForComments(commentsByPostId)
            counterComments += self._getCounterUsersComments(commentsByPostId)
            counterReposts += self._getCounterUsersReposts(postId)
            comments += preparedComments
        bestComments = self._getBestCommentsRating(comments)
        commentLeaderBoard = self._filterLeaderBoardBySubscribers(OrderedDict(self._getCommentLeaderBoard(comments)))

        counters = {
            'like': counterPostLikes + counterCommentLikes,
            'comment': counterComments,
            'repost': counterReposts,
        }

        activeLeaderBoard = self._filterLeaderBoardBySubscribers(OrderedDict(self._getActiveLeaderBoard(counters)))
        leaderBoards = {
            'best_comments': bestComments,
            'comment': commentLeaderBoard,
            'active': activeLeaderBoard,
        }

        image = ImageCls()

        cover = image.createCover(leaderBoards, is_test=True)
        return self.uploader.photo_cover(cover, constants.VK_GROUP_ID, crop_x2=1590, crop_y2=400)

        statsPostId = self._getStatsPostId()
        if statsPostId:
            # self._deletePostById(statsPostId)
            self._unpinPostById(statsPostId)
            time.sleep(0.5)

        res = self.api.method('wall.post', {
            'owner_id': -constants.VK_GROUP_ID,
            'from_group': 1,
            'message': self._createMessage(leaderBoards),
            'attachments': image.loadPhoto(image.createRatingPhoto(leaderBoards, self._createDatePeriod())),
            'signed': 0,
        })
        time.sleep(0.5)
        self._savePostIdToFile(res['post_id'])
        self._pinPostById(res['post_id'])

    def _getStatsPostId(self):
        if os.path.exists(self.fileStatsPostId):
            with open(self.fileStatsPostId, 'r') as f:
                return f.readline().strip()
        return None

    def _deletePostById(self, post_id):
         self.api.method('wall.delete', {
             'owner_id': -constants.VK_GROUP_ID,
             'post_id': str(post_id),
         })

    def _unpinPostById(self, post_id):
        self.api.method('wall.unpin', {
            'owner_id': -constants.VK_GROUP_ID,
            'post_id': str(post_id),
        })

    def _savePostIdToFile(self, postId):
        with open(self.fileStatsPostId, 'w') as f:
            f.write(str(postId))

    def _pinPostById(self, postId):
        self.api.method('wall.pin', {
            'owner_id': -constants.VK_GROUP_ID,
            'post_id': postId,
        })

    def _createDatePeriod(self):
        frm = '%d.%m.%Y'
        date_start = datetime.utcfromtimestamp(self.start_time).strftime(frm)
        date_end = datetime.utcfromtimestamp(self.end_time).strftime(frm)

        return f'{date_start} - {date_end}'

    def _createMessage(self, leaderBoards):
        is_fin = self.utils.checkIsSunday()
        header = f"Финальные рейтинги за неделю {self._createDatePeriod()}" if is_fin else f"Предварительные рейтинги за неделю {self._createDatePeriod()}"

        ratings = f"""
Рейтинг комментариев:
{self._getBestCommentsRatingToStr(leaderBoards['best_comments'])}

Рейтинг комментеров:
{self._leaderBoardToStr(leaderBoards['comment'], 'likes')}

Рейтинг по активности:
{self._leaderBoardToStr(leaderBoards['active'], 'points')}
        """

        return f"""{header}

{ratings}

#rating@mamkin_commenter
"""

    def _filterLeaderBoardBySubscribers(self, leaderBoard):
        filteredLeaderBoard = OrderedDict()
        for id_, val in leaderBoard.items():
            if id_ in self.subscribers:
                filteredLeaderBoard[id_] = val
            # TODO: send message to enter group and sum of lost price
        return filteredLeaderBoard

    def _getActiveLeaderBoard(self, counters):
        rating = Counter()
        for coef_key, coef_val in constants.ACTIVE_COEFFICIENTS.items():
            for cnt_key in counters[coef_key].keys():
                counters[coef_key][cnt_key] *= coef_val
            rating += counters[coef_key]
        return rating.most_common()

    def _getAllUsersRepostsByPostId(self, post_id):
        page = 0
        limit = 1000
        result = []
        while True:
            offset = page * limit
            res = self.api.method('wall.getReposts', {
                'owner_id': -constants.VK_GROUP_ID,
                'post_id': str(post_id),
                'count': limit,
            })
            result += res['profiles']
            if len(res['items']) < offset + limit:
                break
            print(res['count'])
            page += 1
            time.sleep(0.4)

        return [profile['id'] for profile in result]

    def _getAllCommentsByPostId(self, post_id):
        page = 0
        limit = 100
        result = []
        while True:
            offset = page * limit
            res = self.api.method('wall.getComments', {
                'owner_id': -constants.VK_GROUP_ID,
                'post_id': str(post_id),
                'need_likes': 1,
                'count': limit,
            })
            result += res['items']
            if res['count'] < offset + limit:
                break
            print(res['count'])
            page += 1
            time.sleep(0.4)

        return result

    def _getCommentLeaderBoard(self, comments):
        users = {}
        for comment in comments:
            users.setdefault(comment['from_id'], 0)
            users[comment['from_id']] += comment['likes_count']
        return sorted(users.items(), key=lambda item: item[1], reverse=True)[:constants.TOP_NUMBER]

    def _leaderBoardToStr(self, leaderBoard, type, need_prizes=False):
        result = ''
        for i, val in enumerate(leaderBoard.items()):
            id_, likes = val
            prize = f"Приз: {constants.PRIZES[i]} р." if need_prizes else ""
            result += f"{i + 1}. [https://vk.com/id{id_}|{self.utils.getFullNameById([id_])[0]}] - {likes} {type}. {prize}\n"
        return result

    def _getBestCommentsRatingToStr(self, leaderBoard, need_prizes=False):
        result = ''
        for i, val in enumerate(leaderBoard):
            prize = f"Приз: {constants.BEST_COMMENT_PRIZE[i]} р." if need_prizes else ""
            result += f"""{i + 1}. "{val['text']}" от [https://vk.com/id{val['from_id']}|{self.utils.getFullNameById([val['from_id']])[0]}] к [https://vk.com/public196777471?w=wall-196777471_{val['post_id']}|посту] - {val['likes_count']} likes. {prize}\n"""
        return result

    def _prepareComments(self, comments, post_id):
        result = []
        for comment in comments:
            # TODO: change MIN_LIKES_TO_DELETE_COMMENT
            if comment['likes']['count'] < constants.MIN_LIKES_TO_DELETE_COMMENT \
                    and (int(time.time() - int(comment['date']))) > 86400: # 24 hours
                self.api.method('wall.deleteComment', {
                    'owner_id': -constants.VK_GROUP_ID,
                    'comment_id': str(comment['id']),
                })

            if comment['from_id'] in self.subscribers:
                result.append({
                    'from_id': comment['from_id'],
                    'id': comment['id'],
                    'likes_count': self._getOurLikesByCommentId(comment['id']),
                    'text': comment['text'],
                    'post_id': post_id,
                })

        return result

    def _getUsersLikesByObjTypeAndId(self, obj_type, obj_id) -> set:
        page = 0
        limit = 1000
        result = []
        while True:
            offset = page * limit
            res = self.api.method('likes.getList', {
                'type': obj_type,
                'owner_id': -constants.VK_GROUP_ID,
                'item_id': obj_id,
                'count': limit,
            })
            result += res['items']
            if res['count'] < offset + limit:
                break
            print(res['count'])
            page += 1
            time.sleep(0.4)

        return set(result)

    def _getCounterUsersLikesByPostId(self, post_id):
        return Counter(self._getUsersLikesByObjTypeAndId('post', post_id))

    def _getCounterUsersLikesByCommentId(self, comment_id):
        return Counter(self._getUsersLikesByObjTypeAndId('comment', comment_id))

    def _getCounterUsersReposts(self, post_id):
        return Counter(self._getAllUsersRepostsByPostId(post_id))

    def _getCounterUsersComments(self, comments):
        return Counter([comment['from_id'] for comment in comments])

    def _getTotalCounterForComments(self, comments):
        counter = Counter()
        for comment in comments:
            counter += self._getCounterUsersLikesByCommentId(comment['id'])
        return counter

    def _getOurLikesByCommentId(self, comment_id):
        likes = self._getUsersLikesByObjTypeAndId('comment', comment_id)
        return len(likes.intersection(self.subscribers))

    @staticmethod
    def _getBestCommentsRating(comments, min_likes=constants.MIN_LIKES):
        bestComments = sorted(comments, key=lambda x: x['likes_count'], reverse=True)[:constants.TOP_NUMBER]
        return bestComments

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


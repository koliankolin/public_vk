from Classes.image.Unsplash import Unsplash
from Classes.vk.Image import ImageCls
from Classes.vk.Comment import Comment
from Classes.vk.Post import Post

import time
from datetime import datetime, timedelta, date
from pprint import pprint
from Classes.vk.Utils import Utils

def main():
    # mirrorLoader = NewsLoaderMirror('mirror', 5)
    # print(mirrorLoader.getNewsMappers())

    # dt = datetime.now()
    # dt_st = dt - timedelta(days=dt.weekday())
    # start_time = int(time.mktime(dt_st.timetuple()))
    # dt_end = dt_st + timedelta(days=6)
    # end_time = int(time.mktime(dt_end.timetuple()))

    start_time = int(time.mktime(date(2020, 7, 1).timetuple()))
    end_time = int(time.mktime(date(2020, 7, 5).timetuple()))
    # unsplash = Unsplash()
    # print(unsplash.loadImageUrl())
    # image = ImageCls()
    # print(image.loadPhoto())
    # post = Post()
    # print(post.post([int(time.mktime(datetime.now().timetuple())) + 30]))
    comment = Comment(start_time, end_time)
    # try:
    print(comment.getStats())
        # print('Stats was posted :)')
    # except:
    #     print('Something went wrong :(')
    # utils = Utils()
    # print(utils.getFullNameById([3, 4]))

if __name__ == '__main__':
    main()

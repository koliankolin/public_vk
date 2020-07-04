from Classes.vk.Comment import Comment

import time
import datetime
from pprint import pprint


def main():
    # mirrorLoader = NewsLoaderMirror('mirror', 5)
    # print(mirrorLoader.getNewsMappers())
    start_time = int(time.mktime(datetime.date(2020, 7, 1).timetuple()))
    end_time = int(time.mktime(datetime.date(2020, 7, 5).timetuple()))
    comment = Comment(start_time, end_time)
    pprint(comment.getComments())


if __name__ == '__main__':
    main()

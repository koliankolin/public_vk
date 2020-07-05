from Classes.vk.Image import ImageCls

import time
import datetime
from pprint import pprint


def main():
    # mirrorLoader = NewsLoaderMirror('mirror', 5)
    # print(mirrorLoader.getNewsMappers())
    start_time = int(time.mktime(datetime.date(2020, 7, 1).timetuple()))
    end_time = int(time.mktime(datetime.date(2020, 7, 5).timetuple()))
    image = ImageCls('https://images.unsplash.com/photo-1558981420-87aa9dad1c89?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=1080&fit=max&ixid=eyJhcHBfaWQiOjE0NjI0MX0')
    print(image.loadPhoto())
    # comment = Comment(start_time, end_time)
    # pprint(comment.getComments())


if __name__ == '__main__':
    main()

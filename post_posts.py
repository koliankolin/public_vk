from Classes.vk.Post import Post

import time
from datetime import datetime, timedelta, date
import pytz


def createPostDates(hours):
    result = []
    for hour in hours:
        dt = (datetime.combine(date.today(), datetime.min.time()) + timedelta(days=1, hours=hour)).replace(
                tzinfo=pytz.timezone('Europe/Moscow'))
        result.append(
            int(time.mktime(dt.timetuple()))
        )
    return result


def main():
    hour_st = 10
    hour_end = 18
    silent = 2

    dates = createPostDates(range(hour_st, hour_end, silent))

    post = Post()
    post.post(dates)


if __name__ == '__main__':
    main()
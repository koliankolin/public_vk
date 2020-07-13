from Classes.vk.Post import Post
import time
from datetime import datetime, timedelta, date
import pytz
import constants
from Classes.vk.Comment import Comment


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
    # dt = datetime.now()
    # dt_st = dt - timedelta(days=dt.weekday())
    # start_time = int(time.mktime(dt_st.timetuple()))
    # dt_end = dt_st + timedelta(days=6)
    # end_time = int(time.mktime(dt_end.timetuple()))

    start_time = int(time.mktime(date(2020, 7, 1).timetuple()))
    end_time = int(time.mktime(date(2020, 7, 5).timetuple()))

    comment = Comment(start_time, end_time)
    print(comment.getStats())

    if constants.DAYS_LEFT <= 1:
        hour_st = 8
        hour_end = 23
        silent = 3

        dates = createPostDates(range(hour_st, hour_end, silent))
        post = Post()
        print(post.post(dates))


if __name__ == '__main__':
    main()

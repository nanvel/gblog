import arrow

import os.path


rel = lambda p: os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '../..', p)


def path_to_timestamp(path):
    try:
        year, month, day = path.split('/')[-3:]
        day, t = day.split('_')[:2]
        day = int(day)
        hour = int(t[:2])
        minute = int(t[2:])
        return arrow.get(int(year), int(month), day, hour, minute).timestamp, year, month
    except (ValueError, TypeError):
        return None, None, None


def path_to_slug(path):
    slug = path.split('/')[-1]
    return slug.split('.rst')[0]

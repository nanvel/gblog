import arrow

import os.path


rel = lambda p: os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '../..', p)


def path_to_timestamp(path):
    try:
        year, month, day = path.split('/')[-3:]
        year = int(year)
        month = int(month)
        day, t = day.split('_')[:2]
        day = int(day)
        hour = int(t[:2])
        minute = int(t[2:])
        return arrow.get(year, month, day, hour, minute).timestamp
    except (ValueError, TypeError):
        return None

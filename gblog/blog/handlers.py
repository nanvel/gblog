import arrow
import datetime
import json
import sys
import subprocess

from tornado.options import options
from tornado.web import RequestHandler

from ..common.utils import rel


class FeedHandler(RequestHandler):

    def get(self):
        self.write(self.application.redis.get(options.redis_page_key))


class PostHandler(RequestHandler):

    def get(self):
        limit = self.get_argument('limit', 5)
        limit = int(limit)
        a = self.get_argument('a', None)
        b = self.get_argument('b', None)
        if limit > options.page_limit_max or limit < 1:
            limit = options.page_limit_max
        timestamp = (arrow.utcnow() + datetime.timedelta(days=1)).timestamp
        if not a and not b:
            b = timestamp
        a = int(a) if a else None
        b = int(b) if b else None
        if b:
            posts = self.application.redis.zrevrangebyscore(
                name=options.redis_feed_key,
                max=b, min=0, start=0, num=limit,
                withscores=True, score_cast_func=int)
        else:
            posts = self.application.redis.zrevrangebyscore(
                name=options.redis_feed_key,
                max=timestamp, min=a, start=0, num=limit,
                withscores=True, score_cast_func=int)
        for p in posts:
            self.write(p[0])


class CommitHandler(RequestHandler):

    REDIS_UPDATE_TIMEOUT_KEY = 'gblog:update'

    def post(self):
        if self.application.redis.exists(self.REDIS_UPDATE_TIMEOUT_KEY):
            self.write('Success')
            return
        self.application.redis.setex(self.REDIS_UPDATE_TIMEOUT_KEY, 30, 1)
        proc = subprocess.Popen([sys.executable, rel('pullchanges.sh')])
        proc.communicate()

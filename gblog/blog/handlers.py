import arrow
import datetime
import json
import sys
import subprocess

from tornado.options import options
from tornado.web import RequestHandler

from ..common.exceptions import GBlogException
from ..common.utils import rel


class FeedHandler(RequestHandler):

    def get(self):
        self.write(self.application.redis.get(options.redis_page_key))


class PostHandler(RequestHandler):

    def get(self):
        # limit
        limit = self.get_argument('l', 5)
        limit = int(limit)
        # after
        a = self.get_argument('a', None)
        # before
        b = self.get_argument('b', None)
        # timestamp, get single post, raise an exception if not exists
        t = self.get_argument('t', None)
        if limit > options.page_limit_max or limit < 1:
            limit = options.page_limit_max
        timestamp = (arrow.utcnow() + datetime.timedelta(days=1)).timestamp
        if not a and not b and not t:
            b = timestamp
        a = int(a) if a else None
        b = int(b) if b else None
        t = int(t) if t else None
        if t:
            posts = self.application.redis.zrevrangebyscore(
                name=options.redis_feed_key,
                max=t, min=t, start=0, num=1,
                withscores=True)
            if len(posts) != 1:
                raise GBlogException(message='Not found.', status_code=404)
        elif b:
            posts = self.application.redis.zrevrangebyscore(
                name=options.redis_feed_key,
                max=b - 1, min=0, start=0, num=limit,
                withscores=True)
        else:
            posts = self.application.redis.zrangebyscore(
                name=options.redis_feed_key,
                max=timestamp, min=a, start=0, num=limit,
                withscores=True)
        for p in sorted(posts, key=lambda k: -1 * k[1]):
            print p
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

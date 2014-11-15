import arrow
import json

from tornado.options import options
from tornado.web import RequestHandler


class FeedHandler(RequestHandler):

    def get(self):
        self.write(self.application.redis.get(options.redis_page_key))


class PostHandler(RequestHandler):

    def get(self):
        limit = self.get_argument('limit', 2)
        limit = int(limit)
        a = self.get_argument('a', None)
        b = self.get_argument('b', None)
        if limit > options.page_limit_max or limit < 1:
            limit = options.page_limit_max
        timestamp = arrow.utcnow().timestamp
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

import arrow
import json

from tornado.options import options
from tornado.web import RequestHandler


class FeedHandler(RequestHandler):

    def get(self):
        pass


class PostHandler(RequestHandler):

    def get(self):
        limit = self.get_argument('limit', 5)
        limit = int(limit)
        last = self.get_argument('last', None)
        if limit > options.page_limit_max or limit < 1:
            limit = options.page_limit_max
        if not last:
            last = arrow.utcnow().timestamp
        else:
            last = int(last)
        posts = self.application.redis.zrevrangebyscore(
            name=options.redis_feed_key,
            max=last, min=0, start=0, num=limit,
            withscores=True, score_cast_func=int)
        for p in posts:
            self.write(p[0])

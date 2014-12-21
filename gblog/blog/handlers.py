import arrow
import datetime
import json
import sys
import subprocess

from tornado.options import options

from ..common.exceptions import GBlogException
from ..common.utils import rel
from ..common.handlers import GBlogHandler


class FeedHandler(GBlogHandler):

    def get(self):
        self.write(self.application.redis.get(options.redis_home_key))


class PostHandler(GBlogHandler):

    def get(self, timestamp):
        post_key = options.redis_page_key.format(timestamp=timestamp)
        self.write(self.application.redis.get(post_key))


class CommitHandler(GBlogHandler):

    REDIS_UPDATE_TIMEOUT_KEY = 'gblog:update'

    def post(self):
        if self.application.redis.exists(self.REDIS_UPDATE_TIMEOUT_KEY):
            self.write('Success')
            return
        self.application.redis.setex(self.REDIS_UPDATE_TIMEOUT_KEY, 30, 1)
        proc = subprocess.Popen([sys.executable, rel('pullchanges.sh')])
        proc.communicate()

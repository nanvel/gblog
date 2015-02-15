import subprocess

from tornado.options import options

from ..common.exceptions import GBlogException
from ..common.utils import rel
from ..common.handlers import GBlogHandler


class FeedHandler(GBlogHandler):

    def get(self):
        self.write(
            self.application.redis.get(options.redis_home_key).decode('utf-8'))


class BlogPageHandler(GBlogHandler):

    def get(self, timestamp):
        page_key = options.redis_blog_page_key.format(timestamp=timestamp)
        page = self.application.redis.get(page_key)
        if page is None:
            raise GBlogException(reason='Page was not found!', status_code=404)
        self.write(page.decode('utf-8'))


class SimplePageHandler(GBlogHandler):

    def get(self, slug):
        page_key = options.redis_simple_page_key.format(slug=slug)
        page = self.application.redis.get(page_key)
        if page is None:
            raise GBlogException(reason='Page was not found!', status_code=404)
        self.write(page.decode('utf-8'))


class CommitHandler(GBlogHandler):

    REDIS_UPDATE_TIMEOUT_KEY = 'gblog:update'

    def post(self):
        if self.application.redis.exists(self.REDIS_UPDATE_TIMEOUT_KEY):
            self.write('Success')
            return
        self.application.redis.setex(self.REDIS_UPDATE_TIMEOUT_KEY, 30, 1)
        proc = subprocess.Popen(['bash', rel('pullchanges.sh')])
        proc.communicate()

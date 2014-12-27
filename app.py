import redis

from tornado import web, options, ioloop
from gblog.blog.handlers import (
    FeedHandler, BlogPageHandler, SimplePageHandler,
    CommitHandler)
from gblog.common.utils import rel, load_cfg


class GBlogApplication(web.Application):

    def __init__(self, **kwargs):
        kwargs['handlers'] = [
            web.url(r'/', FeedHandler, name='home'),
            web.url(r'/b/(?P<timestamp>\d{10,11})', BlogPageHandler, name='blog_page'),
            web.url(r'/p/(?P<slug>[\w-]{1,20})', SimplePageHandler, name='simple_page'),
            web.url(r'/commit', CommitHandler, name='commit'),
        ]
        kwargs['debug'] = options.options.debug
        kwargs['static_path'] = rel('static')
        kwargs['template_path'] = rel('templates')
        self.redis = self.get_redis_connection()
        super(GBlogApplication, self).__init__(**kwargs)

    def get_redis_connection(self):
        """ Override me for testing purposes """
        return redis.StrictRedis(
            host=options.options.redis_host,
            port=options.options.redis_port,
            db=options.options.redis_db)


if __name__ == '__main__':
    load_cfg()
    application = GBlogApplication()
    application.listen(options.options.port)
    ioloop.IOLoop.instance().start()

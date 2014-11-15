import redis

from tornado import web, options, ioloop

from gblog.blog.handlers import FeedHandler, PostHandler
from gblog.common.utils import rel


class GBlogApplication(web.Application):

    def __init__(self, **kwargs):
        kwargs['handlers'] = [
            web.url(r'/', FeedHandler, name='feed'),
            web.url(r'/post', PostHandler, name='post'),
        ]
        kwargs['debug'] = True
        kwargs['static_path'] = rel('static')
        kwargs['template_path'] = rel('templates')
        self.redis = redis.StrictRedis(
            host=options.options.redis_host,
            port=options.options.redis_port,
            db=options.options.redis_db)
        super(GBlogApplication, self).__init__(**kwargs)


if __name__ == '__main__':
    options.parse_command_line()
    options.parse_config_file(rel('gblog.cfg'))
    application = GBlogApplication()
    application.listen(options.options.port)
    ioloop.IOLoop.instance().start()

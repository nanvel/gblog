import arrow
import fakeredis
import urllib

from app import GBlogApplication
from tornado.options import options
from tornado.testing import AsyncHTTPTestCase


class GBlogTestApplication(GBlogApplication):

    def get_redis_connection(self):
        return fakeredis.FakeStrictRedis()


class BlogHandlersTestCase(AsyncHTTPTestCase):
    """ run tests:
    .. code-block:: bash
        python -m tornado.testing gblog.blog.tests
    """

    PER_PAGE = 3

    def get_app(self):
        self.app = GBlogTestApplication()
        self.app.settings['debug'] = False
        return self.app

    def create_posts(self):
        timestamp = arrow.utcnow().timestamp
        for key in self.app.redis.keys('gblog:*'):
            self.app.redis.delete(key)
        self.posts = []
        for i in xrange(self.PER_PAGE * 4):
            content = u'Post {i}'.format(i=i)
            self.app.redis.zadd(options.redis_feed_key, timestamp + i, content)
            self.posts.append((timestamp + i, content))

    def test_post_handler(self):
        self.create_posts()
        # default: return last n posts
        self.http_client.fetch(
            '{url}?{params}'.format(
                url=self.get_url(self.app.reverse_url('post')),
                params=urllib.urlencode({'l': 3})),
            self.stop, method='GET')
        response = self.wait()
        self.assertEqual(response.code, 200)
        for p in self.posts[-self.PER_PAGE:]:
            self.assertIn(p[1], response.body)
        self.assertNotIn(self.posts[-1-self.PER_PAGE][1], response.body)
        # return posts after specified time
        self.http_client.fetch(
            '{url}?{params}'.format(
                url=self.get_url(self.app.reverse_url('post')),
                params=urllib.urlencode({'l': 3, 'a': self.posts[self.PER_PAGE * 2][0]})),
            self.stop, method='GET')
        response = self.wait()
        self.assertEqual(response.code, 200)
        for p in self.posts[self.PER_PAGE * 2: self.PER_PAGE * 3]:
            self.assertIn(p[1], response.body)
        self.assertNotIn(self.posts[-1][1], response.body)
        # return posts before specified time
        self.http_client.fetch(
            '{url}?{params}'.format(
                url=self.get_url(self.app.reverse_url('post')),
                params=urllib.urlencode({'l': 3, 'b': self.posts[self.PER_PAGE * 2][0]})),
            self.stop, method='GET')
        response = self.wait()
        self.assertEqual(response.code, 200)
        for p in self.posts[self.PER_PAGE: self.PER_PAGE * 2]:
            self.assertIn(p[1], response.body)
        self.assertNotIn(self.posts[-1][1], response.body)
        # retun single post for timestamp
        t = self.posts[self.PER_PAGE][0]
        self.http_client.fetch(
            '{url}?{params}'.format(
                url=self.get_url(self.app.reverse_url('post')),
                params=urllib.urlencode({'l': 3, 't': t})),
            self.stop, method='GET')
        response = self.wait()
        self.assertEqual(response.code, 200)
        for p in self.posts:
            if p[0] == t:
                self.assertIn(p[1], response.body)
                continue
            self.assertNotIn(p[1], response.body)

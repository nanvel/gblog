import arrow
import redis
import os

from app import GBlogApplication
from bs4 import BeautifulSoup
from docutils import io
from docutils.core import publish_programmatically
from gblog.common.utils import rel, path_to_timestamp, path_to_slug
from gblog.common.directives import register_rst_directives
from tornado import options, template


if __name__ == '__main__':
    options.parse_command_line()
    options.parse_config_file(rel('gblog.cfg'))
    r = redis.StrictRedis(
        host=options.options.redis_host,
        port=options.options.redis_port,
        db=options.options.redis_db)
    loader = template.Loader(rel('templates'))
    blog_page_template = loader.load('blog_page.html')
    simple_page_template = loader.load('simple_page.html')
    content_path = rel(options.options.git_folder)
    app = GBlogApplication()
    blog_pages = []
    simple_pages = []
    for root, dirs, files in os.walk(content_path):
        for f in files:
            if f.endswith('.rst'):
                path = os.path.join(root, f)
                created, year, month = path_to_timestamp(path)
                modified = int(os.path.getmtime(path))
                output, pub = publish_programmatically(
                    source_class=io.FileInput, source=None, source_path=path,
                    destination_class=io.StringOutput,
                    destination=None, destination_path=None,
                    reader=None, reader_name='standalone',
                    parser=None, parser_name='restructuredtext',
                    writer=None, writer_name='html',
                    settings=None, settings_spec=None,
                    settings_overrides={
                        'template': rel('templates/html_writer.txt'),
                        'initial_header_level': 1,
                        'doctitle_xform': False},
                    config_section=None, enable_exit_status=False)
                content = output.strip()
                soup = BeautifulSoup(output)
                header = soup.find('h1')
                if not header:
                    continue
                if created:
                    content = blog_page_template.generate(
                        content=content,
                        header=header.text,
                        date=arrow.get(created).strftime('%B %d, %Y'),
                        share_link=app.reverse_url('blog_page', created),
                        github_link='{git_url}/tree/master/{path}'.format(
                            git_url=options.options.git_url,
                            path='/'.join(path.split('/')[-3:])),
                        google_analytics_key=options.options.google_analytics_key)
                    page_key = options.options.redis_blog_page_key.format(timestamp=created)
                else:
                    content = simple_page_template.generate(
                        content=content,
                        header=header.text,
                        share_link=app.reverse_url('simple_page', created),
                        github_link='{git_url}/tree/master/{path}'.format(
                            git_url=options.options.git_url,
                            path='/'.join(path.split('/')[-3:])),
                        google_analytics_key=options.options.google_analytics_key)
                    slug = path_to_slug(path)
                    page_key = options.options.redis_simple_page_key.format(slug=slug)
                r.set(page_key, content)
                # get header
                if created:
                    blog_pages.append((
                        created,
                        arrow.get(created).strftime('%d'),
                        header.text))
                else:
                    simple_pages.append((slug, header.text))
    # prepare index page
    page_template = loader.load('home.html')
    # prepare blog pages (split by dates)
    blog_pages = sorted(blog_pages, key=lambda t: -t[0])
    blog_pages_by_month = []
    month_posts = []
    month_last = None
    for page in blog_pages:
        month = arrow.get(page[0]).strftime('%Y, %B')
        if month_last != month:
            if month_posts:
                blog_pages_by_month.append((month_last, month_posts))
                month_posts = []
        month_posts.append(page)
        month_last = month
    if month_posts:
        blog_pages_by_month.append((month_last, month_posts))
    content = page_template.generate(
        blog_pages=blog_pages_by_month,
        simple_pages=simple_pages,
        reverse_url=app.reverse_url,
        google_analytics_key=options.options.google_analytics_key)
    r.set(options.options.redis_home_key, content)

import arrow
import redis
import os

from app import GBlogApplication
from bs4 import BeautifulSoup
from docutils import io
from docutils.core import publish_programmatically
from gblog.common.utils import rel, path_to_timestamp
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
    post_template = loader.load('post.html')
    content_path = rel(options.options.git_folder)
    app = GBlogApplication()
    pages = []
    for root, dirs, files in os.walk(content_path):
        for f in files:
            if f.endswith('.rst'):
                path = os.path.join(root, f)
                created, year, month = path_to_timestamp(path)
                if not created:
                    continue
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
                content = post_template.generate(
                    content=content,
                    date=arrow.get(created).strftime('%B %d, %Y'),
                    share_link=app.reverse_url('post', created),
                    github_link='{git_url}/tree/master/{path}'.format(
                        git_url=options.options.git_url,
                        path='/'.join(path.split('/')[-3:])))
                page_key = options.options.redis_page_key.format(timestamp=created)
                r.set(page_key, content)
                # get header
                soup = BeautifulSoup(output)
                header = soup.find('h1')
                if header:
                    pages.append((created, header.text))
    # prepare index page
    page_template = loader.load('home.html')
    pages = sorted(pages, key=lambda t: -t[0])
    content = page_template.generate(pages=pages, reverse_url=app.reverse_url)
    r.set(options.options.redis_home_key, content)

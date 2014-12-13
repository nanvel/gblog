import arrow
import redis
import os

from docutils import io
from docutils.core import publish_programmatically
from gblog.common.utils import rel, path_to_timestamp
from gblog.common.directives import register_rst_directives
from tornado import options, template


REDIS_FEED_TEMP_KEY = 'gblog:feed:temp'


if __name__ == '__main__':
    options.parse_command_line()
    options.parse_config_file(rel('gblog.cfg'))
    r = redis.StrictRedis(
        host=options.options.redis_host,
        port=options.options.redis_port,
        db=options.options.redis_db)
    r.delete(REDIS_FEED_TEMP_KEY)
    loader = template.Loader(rel('templates'))
    post_template = loader.load('post.html')
    years = {}
    content_path = rel(options.options.git_folder)
    for root, dirs, files in os.walk(content_path):
        for f in files:
            if f.endswith('.rst'):
                path = os.path.join(root, f)
                created, year, month = path_to_timestamp(path)
                if year in years:
                    if month not in years[year]:
                        years[year].append(month)
                else:
                    years[year] = [month]
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
                        'initial_header_level': 2,
                        'doctitle_xform': False},
                    config_section=None, enable_exit_status=False)
                content = output.strip()
                content = post_template.generate(
                    post_content=content,
                    date=arrow.get(created).strftime('%B %d, %Y'),
                    date_link='#a={timestamp}'.format(timestamp=created - (created % 86400)),
                    share_link='#a={timestamp}&l=1'.format(timestamp=created),
                    github_link='{git_url}/tree/master/{path}'.format(
                        git_url=options.options.git_url,
                        path='/'.join(path.split('/')[-3:])),
                    timestamp=created)
                r.zadd(REDIS_FEED_TEMP_KEY, created, content)
    r.zunionstore(dest=options.options.redis_feed_key, keys=[REDIS_FEED_TEMP_KEY])
    r.delete(REDIS_FEED_TEMP_KEY)
    # prepare index page
    page_template = loader.load('index.html')
    years_list = []
    for y in sorted(years.keys()):
        mons = []
        for m in sorted(years[y]):
            mons.append((m, arrow.get(int(y), int(m), 1).timestamp))
        years_list.append((y, mons))
    content = page_template.generate(years=years_list)
    r.set(options.options.redis_page_key, content)

import redis
import os

from docutils import io
from docutils.core import publish_programmatically
from gblog.common.utils import rel, path_to_timestamp
from gblog.common.directives import register_rst_directives
from tornado import options


REDIS_FEED_TEMP_KEY = 'gblog:feed:temp'


if __name__ == '__main__':
    options.parse_command_line()
    options.parse_config_file(rel('gblog.cfg'))
    r = redis.StrictRedis(
        host=options.options.redis_host,
        port=options.options.redis_port,
        db=options.options.redis_db)
    r.delete(REDIS_FEED_TEMP_KEY)
    for root, dirs, files in os.walk(options.options.content_path):
        for f in files:
            if f.endswith('.rst'):
                path = os.path.join(root, f)
                created = path_to_timestamp(path)
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
                        'template': rel('templates/html_writer.txt')},
                    config_section=None, enable_exit_status=False)
                content = output.strip()
                r.zadd(REDIS_FEED_TEMP_KEY, created, content)
    r.zunionstore(dest=options.options.redis_feed_key, keys=[REDIS_FEED_TEMP_KEY])
    r.delete(REDIS_FEED_TEMP_KEY)

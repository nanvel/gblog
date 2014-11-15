from tornado import options

from .utils import rel
from .directives import register_rst_directives


options.define('port', default=5000, help='Default app port.', type=int)
options.define('redis_host', default=5000, help='Redis host.', type=str)
options.define('redis_port', default=5000, help='Redis port.', type=int)
options.define('redis_db', default=0, help='Redis db number.', type=int)
options.define('content_path', default=rel('content'), help='Content folder.', type=str)
options.define('redis_feed_key', default='gblog:feed', help='Redis feed key.', type=str)
options.define('redis_page_key', default='gblog:page', help='Redis page key.', type=str)
options.define('page_limit_max', default=5, help='Page limit.', type=int)


register_rst_directives()

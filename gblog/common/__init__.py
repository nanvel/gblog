from tornado import options

from .utils import rel
from .directives import register_rst_directives


options.define('port', default=5000, help='Default app port.', type=int)
options.define('redis_host', default=5000, help='Redis host.', type=str)
options.define('redis_port', default=5000, help='Redis port.', type=int)
options.define('redis_db', default=0, help='Redis db number.', type=int)
options.define('content_path', default=rel('content'), help='Content folder.', type=str)
options.define('redis_page_key', default='gblog:page:{timestamp}', help='Redis post page key.', type=str)
options.define('redis_home_key', default='gblog:home', help='Redis home page key.', type=str)
options.define('page_limit_max', default=5, help='Page limit.', type=int)
options.define('google_maps_key', default='', help='Google embed maps key.', type=str)
options.define('git_url', default='', help='Github url.', type=str)
options.define('git_folder', default='', help='Git folder, relative path.', type=str)

register_rst_directives()

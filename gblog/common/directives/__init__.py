from .blockquote import BlockQuote
from .coordinate import Coordinate
from .video import Youtube, Vimeo
from .info import Info

from docutils.parsers.rst import directives


def register_rst_directives():
    directives.register_directive('youtube', Youtube)
    directives.register_directive('vimeo', Vimeo)
    directives.register_directive('info', Info)
    directives.register_directive('blockquote', BlockQuote)
    directives.register_directive('coordinate', Coordinate)


from .video import Youtube, Vimeo

from docutils.parsers.rst import directives


def register_rst_directives():
    directives.register_directive('youtube', Youtube)
    directives.register_directive('vimeo', Vimeo)

# -*- coding: utf-8 -*-
"""
https://gist.github.com/dbrgn/2922648

ReST directive for embedding Youtube and Vimeo videos.

There are two directives added: ``youtube`` and ``vimeo``. The only
argument is the video id of the video to include.

Both directives have three optional arguments: ``height``, ``width``
and ``align``. Default height is 281 and default width is 500.

Example::

    .. youtube:: anwy2MPT5RE
        :height: 315
        :width: 560
        :align: left

:copyright: (c) 2012 by Danilo Bargen.
:license: BSD 3-clause
"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives


def align(argument):
    """Conversion function for the "align" option."""
    return directives.choice(argument, ('left', 'center', 'right'))


class IframeVideo(Directive):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'height': directives.nonnegative_int,
        'width': directives.nonnegative_int,
        'align': align,
        'alt': directives.unchanged,
    }
    default_width = 400

    def run(self):
        self.options['video_id'] = directives.uri(self.arguments[0])
        if not self.options.get('width'):
            self.options['width'] = self.default_width
        # 16x9
        if not self.options.get('height'):
            self.options['height'] = int(self.options['width'] / 16. * 9)
        if not self.options.get('align'):
            self.options['align'] = 'left'
        return [nodes.raw('', self.get_html(), format='html')]


class Youtube(IframeVideo):

    def get_html(self):
        html = '<iframe src="http://www.youtube.com/embed/%(video_id)s" \
frameborder="0" webkitAllowFullScreen mozallowfullscreen allowfullscreen \
class="align-%(align)s" width="%(width)u" height="%(height)u" \
style="margin-top: 20px;"></iframe>'
        return html % self.options


class Vimeo(IframeVideo):

    def get_html(self):
        html = '<iframe src="http://player.vimeo.com/video/%(video_id)s" \
frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen \
class="align-%(align)s" width="%(width)u" height="%(height)u" style="margin-top: 20px;"></iframe>'
        return html % self.options

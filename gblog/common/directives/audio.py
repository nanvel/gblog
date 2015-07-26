# -*- coding: utf-8 -*-
"""
ReST directive for embedding audio html5 element.

Example::

    .. audio:: https://s3-us-west-2.amazonaws.com/nanvel-thai/b/bird_nok.mov
        :alt: Bird - nok
"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives


class HTML5Audio(Directive):

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'alt': directives.unchanged,
    }

    def run(self):
        audio_url = directives.uri(self.arguments[0])
        alt = self.options.get('alt', None)
        alt = ' "{alt}"'.format(alt=alt) if alt else ''
        html = '<audio src="{audio_url}" preload="none"{alt} controls></audio>'.format(
            audio_url=audio_url, alt=alt)
        return [nodes.raw('', html, format='html')]

# -*- coding: utf-8 -*-
"""
Example::

    .. meta::
        :tags: Phuket, Kamala
        :latitude: 12345
        :longitude: 12345
        :place: Kamala beach

"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives


class Info(Directive):
    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'tags': directives.unchanged,
        'place': directives.unchanged,
    }

    def run(self):
        html = u'<meat class="post-meta"'
        if self.options.get('tags'):
            html += ' data-tags="' + self.options['tags'].strip() + '"'
        if self.options.get('place'):
            html += ' data-place="' + self.options['place'].strip() + '"'
        html += '/>'
        return [nodes.raw('', html, format='html')]

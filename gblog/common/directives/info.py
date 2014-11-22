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
    }

    def run(self):
        html = u'<div class="row post_info">'
        if self.options.get('tags'):
            html += '<div class="col-md-12"><div class="tag_area">'
            for tag in self.options['tags'].split(','):
                html += '<a href="#">#{tag}</a>'.format(tag=tag.strip())
            html += '</div></div>'
        html += '</div>'
        return [nodes.raw('', html, format='html')]

# -*- coding: utf-8 -*-
"""
Example::

    .. blockquote::
        :content: Everything should be made as simple<br/>as possible, but not simpler
        :author: Albert Einstein
        :author_url: http://en.wikipedia.org/wiki/Albert_Einstein

"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives


class BlockQuote(Directive):
    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'content': directives.unchanged,
        'author': directives.unchanged,
        'author_url': directives.unchanged,
    }

    def run(self):
        html = u'<div class="sinle_blockquote">'
        html += '<h2><sup>&ldquo;</sup>{content}<sup>&rdquo;</sup></h2>'.format(
            content=self.options['content'])
        if self.options.get('author_url'):
            html += '<a href="{author_url}" target="_blank">{author_name}</a></div>'.format(
                author_url=self.options['author_url'], author_name=self.options['author'])
        else:
            html += '{author_name}</div>'.format(author_name=self.options['author'])
        return [nodes.raw('', html, format='html')]

# -*- coding: utf-8 -*-
"""
Example::

    .. coordinate:: 7.852532 98.347867
        :alt: Tony's restaurant on Chalong, Phuket
        :width: 600
        :height: 450

"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from tornado.options import options


class Coordinate(Directive):
    has_content = False
    required_arguments = 2
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'alt': directives.unchanged,
        'width': directives.nonnegative_int,
        'height': directives.nonnegative_int,
    }

    def run(self):
        latitude, longitude = self.arguments
        latitude = float(latitude.strip())
        longitude = float(longitude.strip())
        if not self.options.get('width'):
            self.options['width'] = 600
        if not self.options.get('height'):
            self.options['height'] = 450
        html = u'<iframe width="{width}" height="{height}" frameborder="0" style="border:0; margin-top: 20px;" '.format(
            width=self.options['width'], height=self.options['height'])
        html += u'src="https://www.google.com/maps/embed/v1/place?'
        html += 'q={latitude:.6f}%2C%20{longitude:.6f}&key={key}"'.format(
            latitude=latitude, longitude=longitude, key=options.google_maps_key)
        if self.options.get('alt'):
            html += ' alt="{alt}"'
        html += '></iframe>'
        return [nodes.raw('', html, format='html')]

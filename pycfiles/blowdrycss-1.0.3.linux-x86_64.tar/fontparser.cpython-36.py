# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/fontparser.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 3019 bytes
from __future__ import absolute_import
__author__ = 'chad nelson'
__project__ = 'blowdrycss'

class FontParser(object):
    __doc__ = " **Features:**\n\n    - Parses unquoted font families.\n\n      Unquoted Font-Family References:\n        | http://www.cssfontstack.com/\n        | https://mathiasbynens.be/notes/unquoted-font-family\n\n    - Holds a basic ``font_families_dict`` (could be extended as desired):\n        | Keys: ``font-family`` category names\n        | Values: ``font-family`` member names\n\n    - Can generate web safe fallback fonts.\n\n    Assumes that the property_name is ``font-family``. It does not handle the shorthand property_name ``font``\n\n    **Examples:**\n\n    >>> font_parser = FontParser('papyrus')\n    >>> font_parser.generate_fallback_fonts()\n    'papyrus, fantasy'\n\n    "

    def __init__(self, font_value=''):
        self.font_value = font_value
        self.font_families_dict = {'serif':{
          'georgia', 'palatino', 'times', 'cambria', 'didot', 'garamond', 'perpetua', 'rockwell', 'baskerville'}, 
         'sans-serif':{
          'arial', 'helvetica', 'gadget', 'cursive', 'impact', 'charcoal', 'tahoma', 'geneva', 'verdana',
          'calibri', 'candara', 'futura', 'optima'}, 
         'monospace':{
          'courier', 'monaco', 'consolas'}, 
         'fantasy':{
          'copperplate', 'papyrus'}}

    def generate_fallback_fonts(self):
        """ Generates web safe fallback fonts

        Reference: http://www.w3schools.com/cssref/css_websafe_fonts.asp

        :return: (str) -- Returns a web safe fallback font string.

        **Examples:**

        >>> font_parser = FontParser('arial')
        >>> font_parser.generate_fallback_fonts()
        'arial, sans-serif'
        >>> font_parser.font_value = 'monospace'
        'monospace'
        >>> font_parser.font_value = 'invalid'
        ''

        """
        fallback = ''
        if self.font_value in self.font_families_dict:
            fallback = self.font_value
        else:
            for family, fonts in self.font_families_dict.items():
                if self.font_value in fonts:
                    fallback = self.font_value + ', ' + family

        return fallback
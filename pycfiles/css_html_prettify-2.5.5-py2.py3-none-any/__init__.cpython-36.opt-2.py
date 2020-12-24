# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /css_html_js_minify/__init__.py
# Compiled at: 2018-04-12 15:13:40
# Size of source mod 2**32: 480 bytes
__doc__ = 'CSS-HTML-JS-Minify.\n\nMinifier for the Web.\n'
from .minify import process_single_html_file, process_single_js_file, process_single_css_file, html_minify, js_minify, css_minify
__version__ = '2.5.5'
__all__ = ('__version__', 'process_single_html_file', 'process_single_js_file', 'process_single_css_file',
           'html_minify', 'js_minify', 'css_minify', 'minify')
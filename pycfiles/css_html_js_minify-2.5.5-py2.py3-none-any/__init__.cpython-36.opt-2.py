# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /css_html_js_minify/__init__.py
# Compiled at: 2018-04-12 15:13:40
# Size of source mod 2**32: 480 bytes
"""CSS-HTML-JS-Minify.

Minifier for the Web.
"""
from .minify import process_single_html_file, process_single_js_file, process_single_css_file, html_minify, js_minify, css_minify
__version__ = '2.5.5'
__all__ = ('__version__', 'process_single_html_file', 'process_single_js_file', 'process_single_css_file',
           'html_minify', 'js_minify', 'css_minify', 'minify')
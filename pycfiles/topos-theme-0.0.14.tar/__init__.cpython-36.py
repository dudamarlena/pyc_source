# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/alcarney/topos-theme/topos_theme/__init__.py
# Compiled at: 2019-03-14 16:16:04
# Size of source mod 2**32: 419 bytes
from os import path
__version__ = '0.0.14'

def update_context(app, pagename, templatename, context, doctree):
    context['topos_theme_version'] = __version__


def setup(app):
    if hasattr(app, 'add_html_theme'):
        app.add_html_theme('topos-theme', path.abspath(path.dirname(__file__)))
    app.connect('html-page-context', update_context)
    return {'version':__version__, 
     'parallel_read_safe':True}
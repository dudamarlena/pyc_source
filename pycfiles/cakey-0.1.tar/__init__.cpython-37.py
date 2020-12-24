# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jose/src/cakephp/docs-theme/cakephp_theme/__init__.py
# Compiled at: 2019-11-29 20:54:07
# Size of source mod 2**32: 552 bytes
import os
__version__ = '1.1.3'

def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return cur_dir


def update_context(app, pagename, templatename, context, doctree):
    context['cakephp_theme_version'] = __version__
    context['branch'] = app.config.branch


def setup(app):
    app.connect('html-page-context', update_context)
    app.add_config_value('branch', '', True)
    return {'version':__version__, 
     'parallel_read_safe':True}
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    return {'version':__version__,  'parallel_read_safe':True}
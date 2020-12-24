# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/hg/public/logilab-sphinx-themes/logilab_sphinx_themes/__init__.py
# Compiled at: 2018-07-17 03:56:14
import os
from logilab_sphinx_themes import _version as version

def get_path():
    """
    Shortcut for users whose theme is next to their conf.py.
    """
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def update_context(app, pagename, templatename, context, doctree):
    context['logilab_sphinx_themes_version'] = version.__version__


def setup(app):
    if hasattr(app, 'add_html_theme'):
        theme_path = os.path.abspath(os.path.dirname(__file__))
        app.add_html_theme('logilab', theme_path)
    app.connect('html-page-context', update_context)
    return {'version': version.__version__, 'parallel_read_safe': True}
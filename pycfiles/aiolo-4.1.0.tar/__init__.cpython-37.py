# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rbw/code/pycharm/aioli-sphinx-theme/alabaster/__init__.py
# Compiled at: 2019-06-28 12:50:14
# Size of source mod 2**32: 741 bytes
import os
from alabaster import _version as version

def get_path():
    """
    Shortcut for users whose theme is next to their conf.py.
    """
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def update_context(app, pagename, templatename, context, doctree):
    context['alabaster_version'] = version.__version__


def setup(app):
    if hasattr(app, 'add_html_theme'):
        theme_path = os.path.abspath(os.path.dirname(__file__))
        app.add_html_theme('alabaster', theme_path)
    app.connect('html-page-context', update_context)
    return {'version':version.__version__, 
     'parallel_read_safe':True}
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/art/projects/allabaster-theme/allabaster/__init__.py
# Compiled at: 2016-07-01 11:25:32
import os
from allabaster import _version as version

def get_path():
    """
    Shortcut for users whose theme is next to their conf.py.
    """
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def update_context(app, pagename, templatename, context, doctree):
    context['allabaster_version'] = version.__version__


def setup(app):
    app.connect('html-page-context', update_context)
    return {'version': version.__version__, 'parallel_read_safe': True}
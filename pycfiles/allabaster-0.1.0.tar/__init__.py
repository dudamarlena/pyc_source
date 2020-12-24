# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
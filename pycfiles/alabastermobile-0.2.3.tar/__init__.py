# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/alabastermobile/alabastermobile/__init__.py
# Compiled at: 2016-10-01 09:06:05
import os
from alabastermobile import _version as version
__version__ = version.__version__

def get_path():
    """
    Shortcut for users whose theme is next to their conf.py.
    """
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def update_context(app, pagename, templatename, context, doctree):
    context['alabastermobile_version'] = version.__version__


def setup(app):
    app.connect('html-page-context', update_context)
    return {'version': version.__version__, 'parallel_read_safe': True}
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idm/Work/flask-diamond/flask_diamond/facets/debugger.py
# Compiled at: 2016-11-26 11:00:21
from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension()

def init_debugger(self):
    """
    Initialize the DebugToolbar

    :returns: None

    The `DebugToolbar <http://flask-
    debugtoolbar.readthedocs.org/en/latest/>`_ is a handy utility for
    debugging your application during development.

    This function obeys the ``DEBUG_TOOLBAR`` configuration setting.  Only
    if this value is explicitly set to True will the Debug Toolbarr run.
    """
    if 'DEBUG_TOOLBAR' in self.app.config and self.app.config['DEBUG_TOOLBAR']:
        toolbar.init_app(self.app)
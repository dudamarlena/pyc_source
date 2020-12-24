# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/server/appengine.py
# Compiled at: 2016-04-25 13:24:08
# Size of source mod 2**32: 554 bytes
"""Python-standard reference servers for development use."""
from __future__ import unicode_literals
import warnings
from google.appengine.ext.webapp.util import run_wsgi_app

def appengine(application):
    """Google App Engine adapter, CGI.
        
        Note: This adapter is essentially untested, and likely duplicates the `cgiref` adapter.
        """
    warnings.warn('Interactive debugging and other persistence-based processes will not work.')
    run_wsgi_app(application)
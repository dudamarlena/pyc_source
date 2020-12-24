# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/webapptitude/__init__.py
# Compiled at: 2016-08-31 16:32:16
"""
Import the core components of standard applications.
"""
import os
from util import is_dev_server, is_prod_server
from test import fix_appengine_sys_path
from version import __version__
if not (is_prod_server() or is_dev_server()):
    fix_appengine_sys_path(noisy=False)
from webapp2 import exc as exceptions
from application import WSGIApplication
from handlers import RequestHandler
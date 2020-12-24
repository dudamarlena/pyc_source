# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/htconsole/wsgiapp.py
# Compiled at: 2006-05-01 04:17:37
import os
from paste.deploy.config import ConfigMiddleware
from wareweb.wsgiapp import make_wareweb_app

def make_app(global_conf, **kw):
    app = make_wareweb_app(global_conf, package_name='htconsole', root_path=os.path.dirname(__file__), **kw)
    return app
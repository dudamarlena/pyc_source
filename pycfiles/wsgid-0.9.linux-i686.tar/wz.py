# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/wsgid/servers/wz.py
# Compiled at: 2009-03-08 14:43:51
from werkzeug.serving import run_simple
from wsgid.server import BaseWSGIServer

class WSGIServer(BaseWSGIServer):
    name = 'Werkzeug'

    def start(self):
        run_simple(self.conf.host, self.conf.port, self.app, processes=1)
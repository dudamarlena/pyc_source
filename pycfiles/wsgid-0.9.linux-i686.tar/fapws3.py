# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/wsgid/servers/fapws3.py
# Compiled at: 2009-03-08 09:55:18
from wsgid.server import BaseWSGIServer
import fapws._evwsgi as evwsgi
from fapws import base

class WSGIServer(BaseWSGIServer):
    name = 'fapws3'

    def start(self):
        evwsgi.start(self.conf.host, self.conf.port)
        evwsgi.set_base_module(base)
        evwsgi.wsgi_cb(('', self.app))
        self.log.info('Starting Fapws3 web server')
        evwsgi.run()

    def stop(self):
        pass
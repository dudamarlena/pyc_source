# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/wsgid/servers/circuitsweb.py
# Compiled at: 2009-03-13 21:11:45
from wsgid.server import BaseWSGIServer
from circuits.web import BaseServer, wsgi
from circuits.core.workers import cpus, processes
from circuits.net.pollers import EPoll, Poll, Select

class WSGIServer(BaseWSGIServer):
    name = 'circuitsweb'

    def start(self):
        self.server = BaseServer(self.conf.port, poller=Select)
        self.server += wsgi.Gateway(self.app)
        for i in xrange(cpus() - 1):
            self.server.start(process=True)

        self.server.run()

    def stop(self):
        self.server.stop()
        for p in processes():
            p.terminate()
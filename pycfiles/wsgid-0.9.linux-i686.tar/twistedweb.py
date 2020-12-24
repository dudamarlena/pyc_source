# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/wsgid/servers/twistedweb.py
# Compiled at: 2009-03-17 21:43:49
from twisted.internet import reactor
from twisted.web import server
from twisted.web.wsgi import WSGIResource
from twisted.python.threadpool import ThreadPool
from twisted.internet import reactor
from wsgid.server import BaseWSGIServer
wsgiThreadPool = ThreadPool()
wsgiThreadPool.start()
reactor.addSystemEventTrigger('after', 'shutdown', wsgiThreadPool.stop)

class WSGIServer(BaseWSGIServer):

    def start(self):
        self.log.info('Starting Twisted web server.')
        wsgi_res = WSGIResource(reactor, wsgiThreadPool, self.app)
        site = server.Site(wsgi_res)
        reactor.listenTCP(self.conf.port, site)
        reactor.run()

    def stop(self):
        self.log.debug('Stopping Twisted web server.')
        reactor.stop()
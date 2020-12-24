# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pumpkin/server.py
# Compiled at: 2014-12-13 05:07:25
"""
Bottle-like Servers strategy.

Method Pumpkin.run accept a subclass of ServerAdapter, create a server 
instance and run applications using the run interface provided by ServerAdapter.

So the server must implement the interface 'run' provided by ServerAdapter.
"""

class ServerAdapter(object):

    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port

    def __repr__(self):
        return '%s (%s:%s)' % (self.__class__.__name__, self.host, self.port)

    def run(self, app):
        pass


class WSGIRefServer(ServerAdapter):

    def run(self, app):
        from wsgiref.simple_server import make_server
        httpd = make_server(self.host, self.port, app)
        httpd.serve_forever()


class TornadoServer(ServerAdapter):
    """Tornado server for test and example.
    """

    def run(self, app):
        import tornado.wsgi, tornado.httpserver, tornado.ioloop
        container = tornado.wsgi.WSGIContainer(app)
        server = tornado.httpserver.HTTPServer(container)
        server.listen(port=self.port, address=self.host)
        tornado.ioloop.IOLoop.instance().start()


class TwistedServer(ServerAdapter):
    """Twisted server for test purpose
    """

    def run(self, app):
        from twisted.web import server, wsgi
        from twisted.internet import reactor
        resource = wsgi.WSGIResource(reactor, reactor.getThreadPool(), app)
        server = server.Site(resource)
        reactor.listenTCP(port=self.port, factory=server, interface=self.host)
        reactor.run()


class WerkzeugServer(ServerAdapter):
    """Werkzeug server for test purpose
    """

    def run(self, app):
        from werkzeug.serving import run_simple
        run_simple(self.host, self.port, app, use_debugger=True, use_reloader=True)
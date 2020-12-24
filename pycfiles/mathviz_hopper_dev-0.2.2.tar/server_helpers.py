# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sam/Documents/fall17/mathviz/mathviz_hopper/src/server_helpers.py
# Compiled at: 2017-11-28 23:03:57
import json
from bottle import Bottle, ServerAdapter
from bottle import route, run, post, request
import threading, time

class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:

            class QuietHandler(WSGIRequestHandler):

                def log_request(*args, **kw):
                    pass

            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        print 'shutting down'
        self.server.shutdown()


if __name__ == '__main__':
    app = Bottle()

    @app.route('/settings')
    def hello():
        return json.dumps({'test': 8})


    @app.route('/query', method='POST')
    def query():
        print 'query'
        print json.loads(request.body.read()).get('query')
        return 'null'


    server = MyWSGIRefServer(host='localhost', port=8088)

    def begin():
        run(app, server=server)


    begin()
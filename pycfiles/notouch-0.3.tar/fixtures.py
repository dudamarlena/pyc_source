# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mcot/Dropbox (Dropbox)/notouch/tests/api_tests/fixtures.py
# Compiled at: 2015-12-08 20:00:32
import pytest, tornado.httpserver, tornado.netutil, socket, threading, random, logging
from notouch.app import Application
from notouch.util import create_database
from notouch.util import clean_database

class Server(object):
    """ Wrapper around Tornado server with test helpers. """

    def __init__(self):
        tornado_settings = {'debug': False}
        self.app = Application(tornado_settings)
        self.app.rethinkdb_db = 'notouch_testing'
        self.rethinkdb_conn = create_database(self.app.rethinkdb_host, self.app.rethinkdb_port, self.app.rethinkdb_db)
        self.server = tornado.httpserver.HTTPServer(self.app)
        self.server.add_sockets(tornado.netutil.bind_sockets(None, 'localhost', family=socket.AF_INET))
        self.server.start()
        self.io_thread = threading.Thread(target=tornado.ioloop.IOLoop.instance().start)
        logging.getLogger('tornado.access').disabled = True
        self.io_thread.start()
        return

    @property
    def port(self):
        return self.server._sockets.values()[0].getsockname()[1]


@pytest.fixture()
def tornado_server(request):
    server = Server()

    def fin():
        tornado.ioloop.IOLoop.instance().stop()
        server.io_thread.join()
        clean_database(server.rethinkdb_conn, server.app.rethinkdb_db, testing=True)

    request.addfinalizer(fin)
    return server
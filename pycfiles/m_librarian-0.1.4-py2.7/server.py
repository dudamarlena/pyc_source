# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.7/m_librarian/web/server.py
# Compiled at: 2018-04-01 15:12:23
import os, sys
from wsgiref import simple_server
from wsgiref.handlers import SimpleHandler
from wsgiref.simple_server import WSGIServer
from bottle import route, run
simple_server.ServerHandler = SimpleHandler

class QuitWSGIServer(WSGIServer):
    _quit_flag = False

    def serve_forever(self):
        while not self._quit_flag:
            self.handle_request()


@route('/quit')
def quit():
    QuitWSGIServer._quit_flag = True
    return 'The program has finished. Have a nice day!'


def run_server(host='localhost', port=0):
    os.chdir(os.path.dirname(__file__))
    sys.path.insert(0, os.getcwd())
    run(host=host, port=port, server_class=QuitWSGIServer, debug=True)
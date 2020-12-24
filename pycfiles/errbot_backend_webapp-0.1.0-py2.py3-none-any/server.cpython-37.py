# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/attakei/works/errbot/devel-plugins/backends/webapp/build/lib/errbot_backend_webapp/server.py
# Compiled at: 2019-06-24 11:07:57
# Size of source mod 2**32: 1577 bytes
"""Backend webserver module
"""
from pathlib import Path
from flask import Flask, request
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from jinja2 import Environment, FileSystemLoader

class WebServer(object):

    def __init__(self):
        self._resources_dir = Path(__file__).parent / 'resources'
        self._app = Flask(__name__,
          static_folder=(self._resources_dir / 'static'))
        self._sockets = Sockets(self._app)

    def configure(self, handler=None):
        self._app.config['SECRET_KEY'] = 'secret'
        self._app.route('/')(self._get_index)
        if handler is None:
            handler = self._sockets_connect
        self._sockets.route('/connect')(handler)

    def run(self, config=None):
        """Run server
        """
        server = pywsgi.WSGIServer((
         config.host, config.port),
          (self._app),
          handler_class=WebSocketHandler)
        server.serve_forever()

    def _get_index(self):
        """Render index document"""
        jinja2_env = Environment(loader=(FileSystemLoader(str(self._resources_dir))))
        template = jinja2_env.get_template('index.html')
        return template.render({'request': request})

    def _sockets_connect(self, ws):
        while not ws.closed:
            message = ws.receive()
            ws.send(message)


if __name__ == '__main__':
    web = WebServer()
    web.configure()
    web.run()
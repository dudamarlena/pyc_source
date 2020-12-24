# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/Cellar/python/2.7.10_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/geventwebsocket/server.py
# Compiled at: 2015-11-13 17:02:49
from gevent.pywsgi import WSGIServer
from .handler import WebSocketHandler
from .logging import create_logger

class WebSocketServer(WSGIServer):
    handler_class = WebSocketHandler
    debug_log_format = '-' * 80 + '\n' + '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' + '%(message)s\n' + '-' * 80

    def __init__(self, *args, **kwargs):
        self.debug = kwargs.pop('debug', False)
        self.pre_start_hook = kwargs.pop('pre_start_hook', None)
        self._logger = None
        self.clients = {}
        super(WebSocketServer, self).__init__(*args, **kwargs)
        return

    def handle(self, socket, address):
        handler = self.handler_class(socket, address, self)
        handler.handle()

    @property
    def logger(self):
        if not self._logger:
            self._logger = create_logger(__name__, self.debug, self.debug_log_format)
        return self._logger
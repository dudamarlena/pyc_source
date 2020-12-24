# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/Cellar/python/2.7.10_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/geventwebsocket/resource.py
# Compiled at: 2015-11-13 17:02:49
import re, warnings
from collections import OrderedDict
from .protocols.base import BaseProtocol
from .exceptions import WebSocketError

class WebSocketApplication(object):
    protocol_class = BaseProtocol

    def __init__(self, ws):
        self.protocol = self.protocol_class(self)
        self.ws = ws

    def handle(self):
        self.protocol.on_open()
        while True:
            try:
                message = self.ws.receive()
            except WebSocketError:
                self.protocol.on_close()
                break

            self.protocol.on_message(message)

    def on_open(self, *args, **kwargs):
        pass

    def on_close(self, *args, **kwargs):
        pass

    def on_message(self, message, *args, **kwargs):
        self.ws.send(message, **kwargs)

    @classmethod
    def protocol_name(cls):
        return cls.protocol_class.PROTOCOL_NAME


class Resource(object):

    def __init__(self, apps=None):
        self.apps = apps if apps else []
        if isinstance(apps, dict) and not isinstance(apps, OrderedDict):
            warnings.warn('Using an unordered dictionary for the app list is discouraged and may lead to undefined behavior.', UserWarning)
            self.apps = [ (path, app) for path, app in apps.iteritems() ]

    def _is_websocket_app(self, app):
        return isinstance(app, type) and issubclass(app, WebSocketApplication)

    def _app_by_path(self, environ_path, is_websocket_request):
        for path, app in self.apps.items():
            if re.match(path, environ_path):
                if is_websocket_request == self._is_websocket_app(app):
                    return app

        return

    def app_protocol(self, path):
        app = self._app_by_path(path, True)
        if hasattr(app, 'protocol_name'):
            return app.protocol_name()
        else:
            return ''

    def __call__(self, environ, start_response):
        environ = environ
        is_websocket_call = 'wsgi.websocket' in environ
        current_app = self._app_by_path(environ['PATH_INFO'], is_websocket_call)
        if current_app is None:
            raise Exception('No apps defined')
        if is_websocket_call:
            ws = environ['wsgi.websocket']
            current_app = current_app(ws)
            current_app.ws = ws
            current_app.handle()
            return []
        else:
            return current_app(environ, start_response)
            return
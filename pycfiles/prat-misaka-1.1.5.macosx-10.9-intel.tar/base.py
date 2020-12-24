# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/Cellar/python/2.7.10_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/geventwebsocket/protocols/base.py
# Compiled at: 2015-11-13 17:02:49


class BaseProtocol(object):
    PROTOCOL_NAME = ''

    def __init__(self, app):
        self._app = app

    def on_open(self):
        self.app.on_open()

    def on_message(self, message):
        self.app.on_message(message)

    def on_close(self, reason=None):
        self.app.on_close(reason)

    @property
    def app(self):
        if self._app:
            return self._app
        raise Exception('No application coupled')

    @property
    def server(self):
        if not hasattr(self.app, 'ws'):
            return None
        else:
            return self.app.ws.handler.server

    @property
    def handler(self):
        if not hasattr(self.app, 'ws'):
            return None
        else:
            return self.app.ws.handler
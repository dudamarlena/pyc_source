# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/flask_websocket.py
# Compiled at: 2017-01-05 23:50:18
"""
    flask_websocket.py
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Damon Chen.
    :license: BSD, see LICENSE for more details.
"""
import json
from collections import defaultdict
from flask import request, current_app as app

class WebSocket(object):

    def __init__(self, app=None):
        self.app = app
        self.event_handlers = defaultdict(list)
        self.raw_message_handler = None
        if app is not None:
            self.init_app(app)
        return

    def init_app(self, app):
        url = app.config.get('WEBSOCKET_URL', '/ws')

        @app.route(url)
        def ws():
            socket = request.environ.get('wsgi.websocket')
            if socket is not None:
                while True:
                    message = socket.receive()
                    if not message:
                        break
                    self.dispatch_message(message)

            return

    def on(self, event):

        def decorator(handler):
            self.event_handlers[event].append(handler)
            return handler

        return decorator

    def on_raw_message(self):

        def decorator(handler):
            self.raw_message_handler = handler
            return handler

        return decorator

    def dispatch(self, event, *args, **kwargs):
        for handler in self.event_handlers[event]:
            handler(*args, **kwargs)

    def dispatch_message(self, message):
        if self.raw_message_handler is not None:
            self.raw_message_handler(message)
        else:
            try:
                try:
                    msg = json.loads(message)
                except Exception as e:
                    app.logger.error(e)
                else:
                    event = msg.get('event')
                    self.dispatch(event, msg.get('data'))

            finally:
                pass

        return
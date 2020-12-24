# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pycommunicate\proxies\socket.py
# Compiled at: 2016-06-10 20:50:57
from ..util import random_alphanumeric_string

class SocketInterface:

    def __init__(self, controller):
        self.controller = controller

    def request(self, event_id, *args):
        tag = random_alphanumeric_string(75)
        while tag in self.controller.app.socketio.awaited_responses:
            tag = random_alphanumeric_string(75)

        self.controller.app.socketio.send(event_id, self.controller.user.request_id, args, tag=tag)
        return self.controller.app.socketio.await_response(tag)

    def send(self, event_id, *args):
        self.controller.app.socketio.send(event_id, self.controller.user.request_id, args)
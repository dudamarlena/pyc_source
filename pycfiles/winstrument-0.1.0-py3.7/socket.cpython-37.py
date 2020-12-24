# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winstrument\modules\socket.py
# Compiled at: 2019-08-23 17:51:28
# Size of source mod 2**32: 1079 bytes
import sys, frida
from winstrument.base_module import BaseInstrumentation

class Socket(BaseInstrumentation):
    modulename = 'socket'

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.sockets = []

    def on_message(self, message, data):
        if message['type'] == 'send':
            payload = message['payload']
            self.write_message(payload)
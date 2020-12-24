# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winstrument\modules\com_hijack.py
# Compiled at: 2019-08-23 17:51:28
# Size of source mod 2**32: 1214 bytes
from winstrument.base_module import BaseInstrumentation

class ComHijack(BaseInstrumentation):
    modulename = 'com_hijack'

    def __init__(self, *args, **kwargs):
        self._output = []
        (super().__init__)(*args, **kwargs)

    def on_message(self, message, data):
        if message['type'] == 'error':
            print(f"Error: {message}")
            return
        if message['type'] == 'send':
            payload = message['payload']
            self.write_message(payload)

    def get_output(self):
        return self._output
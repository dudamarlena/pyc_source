# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winstrument\modules\process.py
# Compiled at: 2019-08-23 17:51:28
# Size of source mod 2**32: 1184 bytes
import frida, win32con
from winstrument.base_module import BaseInstrumentation

class Process(BaseInstrumentation):
    modulename = 'process'

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
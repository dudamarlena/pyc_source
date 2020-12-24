# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winstrument\modules\registry.py
# Compiled at: 2019-08-23 17:51:28
# Size of source mod 2**32: 1642 bytes
import frida, win32con
from winstrument.base_module import BaseInstrumentation

class Registry(BaseInstrumentation):
    modulename = 'registry'
    HKEY_CONSTANTS = {win32con.HKEY_CURRENT_USER: 'HKEY_CURRENT_USER', win32con.HKEY_LOCAL_MACHINE: 'HKEY_LOCAL_MACHINE', win32con.HKEY_CLASSES_ROOT: 'HKEY_CLASSES_ROOT', win32con.HKEY_USERS: 'HKEY_USERS', win32con.HKEY_CURRENT_CONFIG: 'HKEY_CURRENT_CONFIG'}

    def __init__(self, *args, **kwargs):
        self._output = []
        (super().__init__)(*args, **kwargs)

    def on_message(self, message, data):
        if message['type'] == 'error':
            print(f"Error: {message}")
            return
        if message['type'] == 'send':
            payload = message['payload']
            try:
                if payload['hkey'] in self.HKEY_CONSTANTS:
                    payload['hkey'] = self.HKEY_CONSTANTS[payload['hkey']]
            except KeyError:
                pass

            self.write_message(payload)
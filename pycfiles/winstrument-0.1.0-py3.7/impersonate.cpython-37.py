# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winstrument\modules\impersonate.py
# Compiled at: 2020-02-05 20:03:04
# Size of source mod 2**32: 1434 bytes
from winstrument.base_module import BaseInstrumentation
import win32security

class Impersonate(BaseInstrumentation):
    modulename = 'impersonate'

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)

    def on_message(self, message, data):
        if message['type'] == 'error':
            print(message)
        else:
            payload = message['payload']
            token = message['token']
            sid = win32security.GetTokenInformation(token, win32security.TokenUser)[0]
            name, domain, _ = win32security.LookupAccountSid(None, sid)
            user = f"{domain}\\{name}"
            data = {'function':payload['function'],  'user':user}
            self.write_message(data)
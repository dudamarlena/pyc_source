# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\tools\network\client.py
# Compiled at: 2020-03-18 12:13:39
# Size of source mod 2**32: 937 bytes
from reapy.errors import DisconnectedClientError, DistError
from reapy.tools import json
from .socket import Socket

class Client(Socket):

    def __init__(self, port, host='localhost'):
        super().__init__()
        self._connect(port, host)
        self.port, self.host = port, host

    def _connect(self, port, host):
        super().connect((host, port))
        self.address = self.recv(timeout=None).decode('ascii')

    def _get_result(self):
        s = self.recv(timeout=None).decode()
        return json.loads(s)

    def request(self, function, input=None):
        request = {'function':function, 
         'input':input}
        request = json.dumps(request).encode()
        self.send(request)
        result = self._get_result()
        if result['type'] == 'result':
            return result['value']
        if result['type'] == 'error':
            raise DistError(result['traceback'])
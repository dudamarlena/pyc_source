# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\tools\network\server.py
# Compiled at: 2020-03-18 12:13:39
# Size of source mod 2**32: 4224 bytes
"""Define Server class."""
import reapy
from reapy.tools import json
from .socket import Socket
import socket, traceback

class Server(Socket):
    __doc__ = '\n    Server part of the ``reapy`` dist API.\n\n    It is instantiated inside REAPER. It receives and processes API\n    call requests coming from the outside.\n    '

    def __init__(self, port):
        super().__init__()
        self.bind(('0.0.0.0', port))
        self.listen()
        self.connections = {}
        self.settimeout(0.0001)

    @Socket._non_blocking
    def _get_request(self, connection, address):
        try:
            request = connection.recv()
            request = json.loads(request.decode())
        except (ConnectionAbortedError, ConnectionResetError):
            input = {'args':(address,),  'kwargs':{}}
            request = {'function':self.disconnect, 
             'input':input}

        return request

    def _hold_connection(self, address):
        connection = self.connections[address]
        result = {'type':'result',  'value':None}
        self._send_result(connection, result)
        request = self._get_request(connection, address)
        while request is None or request['function'] != 'RELEASE':
            if request is None:
                request = self._get_request(connection, address)
                continue
            result = self._process_request(request, address)
            try:
                self._send_result(connection, result)
                request = self._get_request(connection, address)
            except (ConnectionAbortedError, ConnectionResetError):
                request = {'function': 'RELEASE'}

        result = {'type':'result', 
         'value':None}
        return result

    def _process_request(self, request, address):
        if request['function'] == 'HOLD':
            return self._hold_connection(address)
        args, kwargs = request['input']['args'], request['input']['kwargs']
        result = {}
        try:
            result['value'] = (request['function'])(*args, **kwargs)
            result['type'] = 'result'
        except Exception:
            result['traceback'] = traceback.format_exc()
            result['type'] = 'error'

        return result

    def _send_result(self, connection, result):
        result = json.dumps(result).encode()
        connection.send(result)

    @Socket._non_blocking
    def accept(self, *args, **kwargs):
        connection, address = super().accept()
        self.connections[address] = connection
        connection.send('{}'.format(address).encode('ascii'))
        return (connection, address)

    def disconnect(self, address):
        connection = self.connections[address]
        connection.shutdown(socket.SHUT_RDWR)
        connection.close()
        del self.connections[address]

    def get_requests(self):
        requests = {}
        for address, connection in self.connections.items():
            request = self._get_request(connection, address)
            if request is not None:
                requests[address] = request

        return requests

    def process_requests(self, requests):
        results = {}
        for address, request in requests.items():
            result = self._process_request(request, address)
            results[address] = result

        return results

    def send_results(self, results):
        for address, result in results.items():
            try:
                connection = self.connections[address]
                self._send_result(connection, result)
            except (KeyError, BrokenPipeError, ConnectionAbortedError, ConnectionResetError):
                pass
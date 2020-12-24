# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/despres/MAIN/Users/despres/Desktop/reaper/scripts/reapy/reapy/reascript_api/network/server.py
# Compiled at: 2019-02-23 09:59:14
# Size of source mod 2**32: 4281 bytes
"""Define Server class."""
import reapy
from reapy import reascript_api as RPR
from reapy.tools import json
from .socket import Socket
import socket, traceback
if reapy.is_inside_reaper():
    from reapy.tools.program import Program

class Server(Socket):
    __doc__ = '\n    Server part of the ``reapy`` dist API.\n\n    It is instantiated inside REAPER. It receives and processes API\n    call requests coming from the outside.\n    '

    def __init__(self, port):
        super(Server, self).__init__()
        self.bind(('', port))
        self.listen()
        self.connections = {}
        self.settimeout(0.0001)

    @Socket._non_blocking
    def _get_request(self, connection, address):
        try:
            request = connection.recv()
            request = json.loads(request.decode())
        except (ConnectionAbortedError, ConnectionResetError):
            code = 'server.disconnect(address)'
            program = Program(code).to_dict()
            input = {'address': address, 'server': self}
            request = {'program': program, 'input': input}

        return request

    def _hold_connection(self, address):
        connection = self.connections[address]
        result = {'type': 'result', 'value': None}
        self._send_result(connection, result)
        request = self._get_request(connection, address)
        while request is None or request['program'][0] != 'RELEASE':
            if request is None:
                request = self._get_request(connection, address)
                continue
                result = self._process_request(request, address)
                try:
                    self._send_result(connection, result)
                    request = self._get_request(connection, address)
                except (ConnectionAbortedError, ConnectionResetError):
                    request = {'program': ['RELEASE']}

        result = {'type': 'result', 'value': None}
        return result

    def _process_request(self, request, address):
        if request['program'][0] == 'HOLD':
            return self._hold_connection(address)
        program = Program(*request['program'])
        result = {}
        request['input'].update({'RPR': RPR, 'reapy': reapy})
        try:
            result['value'] = program.run(**request['input'])
            result['type'] = 'result'
        except Exception:
            result['traceback'] = traceback.format_exc()
            result['type'] = 'error'

        return result

    def _send_result(self, connection, result):
        result = json.dumps(result).encode()
        connection.send(result)

    @Socket._non_blocking
    def accept(self):
        connection, address = super(Server, self).accept()
        self.connections[address] = connection
        connection.send('{}'.format(address).encode('ascii'))

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
            except KeyError:
                pass
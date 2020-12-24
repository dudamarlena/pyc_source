# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/despres/MAIN/Users/despres/Desktop/reaper/scripts/reapy/reapy/reascript_api/network/client.py
# Compiled at: 2019-03-03 05:02:52
# Size of source mod 2**32: 1477 bytes
from reapy.errors import DisconnectedClientError, DistError
from reapy.tools import json
from .socket import Socket

class Client(Socket):

    def __init__(self, port):
        super(Client, self).__init__()
        self._connect(port)

    def _connect(self, port):
        super(Client, self).connect(('localhost', port))
        self.address = self.recv(timeout=None).decode('ascii')

    def _get_result(self):
        s = self.recv(timeout=None).decode()
        return json.loads(s)

    def run_program(self, program, input):
        """
        Send a program to the server and return its output.

        Parameters
        ----------
        program : reapy.tools.Program
            Program to run.
        input : dict
            Input to the program.

        Returns
        -------
        result
            Program output

        Raises
        ------
        DistError
            When an error occurs while the server runs the program, its
            traceback is sent to the client and used to raise a
            DistError.
        """
        program = program.to_dict()
        request = {'program': program, 'input': input}
        request = json.dumps(request).encode()
        self.send(request)
        result = self._get_result()
        if result['type'] == 'result':
            return result['value']
        if result['type'] == 'error':
            raise DistError(result['traceback'])
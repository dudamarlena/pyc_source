# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/sphirewallapi/sphirewall_connection.py
# Compiled at: 2018-06-20 19:57:46
from _socket import SOCK_STREAM, AF_INET, AF_UNIX, socket
import json

class SphirewallSocketTransportProvider:
    """ This is the standard socket transport provider for Sphirewall. It passes requests via a socket
        connection directly to Sphirewall. Exceptions thrown here by the socket libraries will
        be caught by the Sphirewall Api and rethrown as a TransportProviderException.

        Normally operates on port 8001
    """
    hostname = None
    port = None

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def send(self, data):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.hostname, int(self.port)))
        s.sendall(json.dumps(data) + '\n')
        response_buffer = ''
        while 1:
            data = s.recv(4096)
            if not data:
                break
            response_buffer += data

        return response_buffer


class SphirewallUnixSocketTransportProvider:
    """ This is the standard unix socket transport provider for Sphirewall. It passes requests via a socket
        connection directly to Sphirewall. Exceptions thrown here by the socket libraries will
        be caught by the Sphirewall Api and rethrown as a TransportProviderException.

    """

    def __init__(self):
        pass

    def send(self, data):
        s = socket(AF_UNIX, SOCK_STREAM)
        s.connect('/var/run/sphirewalld.ctl')
        s.sendall(json.dumps(data) + '\n')
        response_buffer = ''
        while 1:
            data = s.recv(4096)
            if not data:
                break
            response_buffer += data

        return response_buffer
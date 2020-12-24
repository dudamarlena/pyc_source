# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/py3o/renderers/pyuno/main.py
# Compiled at: 2014-11-07 06:57:00
"""
Convertor is a class that handles document exports to other formats
"""
import atexit
from py3o.renderers.pyuno.office import OfficeServer, OfficeClient

def kill_office_server(server):
    server.die()


class Convertor(object):

    def __init__(self, host='localhost', port=2002, **kwargs):
        """the convertor needs to connect to an existing OpenOffice
        server.

        @param host: the hostname/ip address where we can find an open office
        instance
        @type host: string

        @param port: the TCP port to use to connect to the open office instance
        @type port: string or integer
        """
        self.host = host
        self.port = port
        self.server = OfficeServer(host, port, **kwargs)
        self.client = OfficeClient(host, port, **kwargs)

    def _init_server(self):
        if not self.server.is_running():
            self.server.start()
            atexit.register(kill_office_server, self.server)

    def convert(self, infilename, outfilename, format=None):
        self._init_server()
        self.client.convert(infilename, outfilename, format)
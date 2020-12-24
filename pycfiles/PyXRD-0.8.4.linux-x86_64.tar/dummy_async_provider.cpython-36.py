# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/asynchronous/dummy_async_provider.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 883 bytes
from .dummy_async_server import DummyAsyncServer

class DummyAsyncServerProvider(object):
    _server = DummyAsyncServer()

    @classmethod
    def get_status(cls):
        """ should return a three-tuple consisting of the status colour, label and a description:
            ("#FF0000", "Error", "Nameserver not running")
        """
        return ('#00FF00', 'Connected (Dummy)', 'Succesfully connected to Dummy PyXRD Server')

    @classmethod
    def get_server(cls):
        return cls._server

    @classmethod
    def launch_server(cls):
        if cls._server is None:
            cls._server = DummyAsyncServer()

    @classmethod
    def stop_server(cls):
        cls._server.shutdown()
        del cls._server
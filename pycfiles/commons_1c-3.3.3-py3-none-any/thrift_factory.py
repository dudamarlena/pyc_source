# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/commonslib/thrift_factory.py
# Compiled at: 2015-04-04 05:19:06
from thrift.transport import TTransport
from thrift.transport.TSocket import TSocket
__author__ = 'freeway'

class ThriftClientFactory(object):
    _protocols = {}
    _transports = {}

    @classmethod
    def get_transport(cls, host, port):
        key = ('{0}:{1}').format(host, port)
        transport = cls._transports.get(key, None)
        if transport is None:
            socket = TSocket(host, port)
            transport = TTransport.TBufferedTransport(socket)
            transport.open()
            cls._transports[key] = transport
        return transport

    @classmethod
    def clean_all(cls):
        for transport in cls._transports.values():
            transport.close()

        cls._transports.clear()
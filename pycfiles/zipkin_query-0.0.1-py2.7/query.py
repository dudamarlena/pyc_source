# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/zipkin_query/query.py
# Compiled at: 2015-01-08 20:54:38
import sys, os
sys.path.append(os.path.split(os.path.realpath(__file__))[0])
import zipkinQuery.ZipkinQuery
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class Api(object):
    """docstring for Api"""

    def __init__(self, host='10.202.76.52', port=8411):
        self.host = host
        self.port = port
        socket = TSocket.TSocket(host, port)
        self.transport = TTransport.TFramedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(trans=self.transport, strictRead=False, strictWrite=False)
        self.client = zipkinQuery.ZipkinQuery.Client(protocol)
        self.transport.open()

    def conncet(self):
        return self.client

    def close(self):
        self.transport.close()
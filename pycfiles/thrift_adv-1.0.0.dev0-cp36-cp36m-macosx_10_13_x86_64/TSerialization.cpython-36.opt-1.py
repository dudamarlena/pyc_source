# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/TSerialization.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 1389 bytes
from .protocol import TBinaryProtocol
from .transport import TTransport

def serialize(thrift_object, protocol_factory=TBinaryProtocol.TBinaryProtocolFactory()):
    transport = TTransport.TMemoryBuffer()
    protocol = protocol_factory.getProtocol(transport)
    thrift_object.write(protocol)
    return transport.getvalue()


def deserialize(base, buf, protocol_factory=TBinaryProtocol.TBinaryProtocolFactory()):
    transport = TTransport.TMemoryBuffer(buf)
    protocol = protocol_factory.getProtocol(transport)
    base.read(protocol)
    return base
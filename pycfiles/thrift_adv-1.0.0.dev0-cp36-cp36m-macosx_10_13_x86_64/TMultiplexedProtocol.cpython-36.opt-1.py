# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/protocol/TMultiplexedProtocol.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 1457 bytes
from thrift.Thrift import TMessageType
from thrift.protocol import TProtocolDecorator
SEPARATOR = ':'

class TMultiplexedProtocol(TProtocolDecorator.TProtocolDecorator):

    def __init__(self, protocol, serviceName):
        self.serviceName = serviceName

    def writeMessageBegin(self, name, type, seqid):
        if type == TMessageType.CALL or type == TMessageType.ONEWAY:
            super(TMultiplexedProtocol, self).writeMessageBegin(self.serviceName + SEPARATOR + name, type, seqid)
        else:
            super(TMultiplexedProtocol, self).writeMessageBegin(name, type, seqid)
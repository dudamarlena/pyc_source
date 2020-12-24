# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/TMultiplexedProcessor.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 2233 bytes
from thrift.Thrift import TProcessor, TMessageType, TException
from thrift.protocol import TProtocolDecorator, TMultiplexedProtocol

class TMultiplexedProcessor(TProcessor):

    def __init__(self):
        self.services = {}

    def registerProcessor(self, serviceName, processor):
        self.services[serviceName] = processor

    def process(self, iprot, oprot):
        name, type, seqid = iprot.readMessageBegin()
        if type != TMessageType.CALL:
            if type != TMessageType.ONEWAY:
                raise TException('TMultiplexed protocol only supports CALL & ONEWAY')
        index = name.find(TMultiplexedProtocol.SEPARATOR)
        if index < 0:
            raise TException('Service name not found in message name: ' + name + '. Did you forget to use TMultiplexedProtocol in your client?')
        serviceName = name[0:index]
        call = name[index + len(TMultiplexedProtocol.SEPARATOR):]
        if serviceName not in self.services:
            raise TException('Service name not found: ' + serviceName + '. Did you forget to call registerProcessor()?')
        standardMessage = (call, type, seqid)
        return self.services[serviceName].process(StoredMessageProtocol(iprot, standardMessage), oprot)


class StoredMessageProtocol(TProtocolDecorator.TProtocolDecorator):

    def __init__(self, protocol, messageBegin):
        self.messageBegin = messageBegin

    def readMessageBegin(self):
        return self.messageBegin
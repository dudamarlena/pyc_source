# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pypomelo/protocol.py
# Compiled at: 2019-01-03 22:45:52
"""Pomelo protocol See :

https://github.com/NetEase/pomelo/wiki/Communication-Protocol

"""
from __future__ import absolute_import, division, print_function, with_statement
import struct, json
from pypomelo.message import Message

class Protocol(object):
    """A implementation of pomelo protocol.

    +++++++++++++++++++++++++++++++++++++++
    + type +    length    +      body     +
    +++++++++++++++++++++++++++++++++++++++
     1 bytes    3 bytes      length bytes
                big end

    """
    PROTO_TYPE_SYC = 1
    PROTO_TYPE_ACK = 2
    PROTO_TYPE_HEARTBEAT = 3
    PROTO_TYPE_DATA = 4
    PROTO_TYPE_FIN = 5
    DICT_VERSION = None
    DICT_ROUTE_TO_CODE = None
    DICT_CODE_TO_ROUTE = None
    PROTOBUF_VERSION = None
    PROTOBUF_SERVER = None
    PROTOBUF_CLIENT = None

    def __init__(self, proto_type, data=''):
        self.proto_type = proto_type
        self.data = data
        self.length = len(data)

    def head(self):
        """Encode protocol head
        """
        return '%s%s' % (struct.pack('B', self.proto_type), struct.pack('>I', len(self.data))[1:])

    def body(self):
        return self.data

    def append(self, data):
        """When a protocol data package is sent by TCP,
        We could know protocol type and body length from
        first TCP frame.

        Then append other body data from more TCP frames
        until length of body equal length of protocol head
        """
        data_len = len(self.data)
        if data_len >= self.length:
            return False
        need_len = min(self.length - data_len, len(data))
        self.data += data[:need_len]
        return len(self.data) < self.length

    def __add__(self, data):
        self.append(data)
        return self

    def completed(self):
        return len(self.data) >= self.length

    def pack(self):
        return '%s%s' % (self.head(), self.body())

    def __len__(self):
        return self.length

    @classmethod
    def unpack(cls, data):
        """Decode protocol

        Return a new instance of Protocol
        data must be the first frame
        """
        head = data[:4]
        proto_type = struct.unpack('B', head[0])[0]
        body_len = struct.unpack('>I', '\x00' + head[1:])[0]
        proto = cls(proto_type, data[4:])
        proto.length = body_len
        return proto

    @classmethod
    def syc(cls, sys_type, sys_version, user_data={}):
        return cls(cls.PROTO_TYPE_SYC, json.dumps({'sys': {'version': sys_version, 
                   'type': sys_type}, 
           'user': user_data}))

    @classmethod
    def ack(cls):
        return cls(cls.PROTO_TYPE_ACK)

    @classmethod
    def heartbeat(cls):
        return cls(cls.PROTO_TYPE_HEARTBEAT)
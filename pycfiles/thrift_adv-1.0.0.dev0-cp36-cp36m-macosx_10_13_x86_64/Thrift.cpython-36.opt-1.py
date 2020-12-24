# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/Thrift.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 5449 bytes
import sys

class TType(object):
    STOP = 0
    VOID = 1
    BOOL = 2
    BYTE = 3
    I08 = 3
    DOUBLE = 4
    I16 = 6
    I32 = 8
    I64 = 10
    STRING = 11
    UTF7 = 11
    STRUCT = 12
    MAP = 13
    SET = 14
    LIST = 15
    UTF8 = 16
    UTF16 = 17
    _VALUES_TO_NAMES = ('STOP', 'VOID', 'BOOL', 'BYTE', 'DOUBLE', None, 'I16', None,
                        'I32', None, 'I64', 'STRING', 'STRUCT', 'MAP', 'SET', 'LIST',
                        'UTF8', 'UTF16')


class TMessageType(object):
    CALL = 1
    REPLY = 2
    EXCEPTION = 3
    ONEWAY = 4


class TProcessor(object):
    __doc__ = 'Base class for processor, which works on two streams.'

    def process(self, iprot, oprot):
        pass


class TException(Exception):
    __doc__ = 'Base class for all thrift exceptions.'
    if (2, 6, 0) <= sys.version_info < (3, 0):

        def _get_message(self):
            return self._message

        def _set_message(self, message):
            self._message = message

        message = property(_get_message, _set_message)

    def __init__(self, message=None):
        Exception.__init__(self, message)
        self.message = message


class TApplicationException(TException):
    __doc__ = 'Application level thrift exceptions.'
    UNKNOWN = 0
    UNKNOWN_METHOD = 1
    INVALID_MESSAGE_TYPE = 2
    WRONG_METHOD_NAME = 3
    BAD_SEQUENCE_ID = 4
    MISSING_RESULT = 5
    INTERNAL_ERROR = 6
    PROTOCOL_ERROR = 7
    INVALID_TRANSFORM = 8
    INVALID_PROTOCOL = 9
    UNSUPPORTED_CLIENT_TYPE = 10

    def __init__(self, type=UNKNOWN, message=None):
        TException.__init__(self, message)
        self.type = type

    def __str__(self):
        if self.message:
            return self.message
        else:
            if self.type == self.UNKNOWN_METHOD:
                return 'Unknown method'
            else:
                if self.type == self.INVALID_MESSAGE_TYPE:
                    return 'Invalid message type'
                else:
                    if self.type == self.WRONG_METHOD_NAME:
                        return 'Wrong method name'
                    else:
                        if self.type == self.BAD_SEQUENCE_ID:
                            return 'Bad sequence ID'
                        else:
                            if self.type == self.MISSING_RESULT:
                                return 'Missing result'
                            if self.type == self.INTERNAL_ERROR:
                                return 'Internal error'
                            if self.type == self.PROTOCOL_ERROR:
                                return 'Protocol error'
                        if self.type == self.INVALID_TRANSFORM:
                            return 'Invalid transform'
                    if self.type == self.INVALID_PROTOCOL:
                        return 'Invalid protocol'
                if self.type == self.UNSUPPORTED_CLIENT_TYPE:
                    return 'Unsupported client type'
            return 'Default (unknown) TApplicationException'

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.message = iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 2:
                    if ftype == TType.I32:
                        self.type = iprot.readI32()
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        oprot.writeStructBegin('TApplicationException')
        if self.message is not None:
            oprot.writeFieldBegin('message', TType.STRING, 1)
            oprot.writeString(self.message)
            oprot.writeFieldEnd()
        if self.type is not None:
            oprot.writeFieldBegin('type', TType.I32, 2)
            oprot.writeI32(self.type)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()


class TFrozenDict(dict):
    __doc__ = 'A dictionary that is "frozen" like a frozenset'

    def __init__(self, *args, **kwargs):
        (super(TFrozenDict, self).__init__)(*args, **kwargs)
        self._TFrozenDict__hashval = hash(TFrozenDict) ^ hash(tuple(sorted(self.items())))

    def __setitem__(self, *args):
        raise TypeError("Can't modify frozen TFreezableDict")

    def __delitem__(self, *args):
        raise TypeError("Can't modify frozen TFreezableDict")

    def __hash__(self):
        return self._TFrozenDict__hashval
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/protocol/TBase.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 2827 bytes
from thrift.transport import TTransport

class TBase(object):
    __slots__ = ()

    def __repr__(self):
        L = ['%s=%r' % (key, getattr(self, key)) for key in self.__slots__]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            for attr in self.__slots__:
                my_val = getattr(self, attr)
                other_val = getattr(other, attr)
                if my_val != other_val:
                    return False

            return True

    def __ne__(self, other):
        return not self == other

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
        else:
            iprot.readStruct(self, self.thrift_spec)

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
        else:
            oprot.writeStruct(self, self.thrift_spec)


class TExceptionBase(TBase, Exception):
    pass


class TFrozenBase(TBase):

    def __setitem__(self, *args):
        raise TypeError("Can't modify frozen struct")

    def __delitem__(self, *args):
        raise TypeError("Can't modify frozen struct")

    def __hash__(self, *args):
        return hash(self.__class__) ^ hash(self.__slots__)

    @classmethod
    def read(cls, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and cls.thrift_spec is not None:
            self = cls()
            return iprot._fast_decode(None, iprot, [
             self.__class__, self.thrift_spec])
        else:
            return iprot.readStruct(cls, cls.thrift_spec, True)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/protocol/TCompactProtocol.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 14749 bytes
from .TProtocol import TType, TProtocolBase, TProtocolException, checkIntegerLimits
from struct import pack, unpack
from ..compat import binary_to_str, str_to_binary
__all__ = [
 'TCompactProtocol', 'TCompactProtocolFactory']
CLEAR = 0
FIELD_WRITE = 1
VALUE_WRITE = 2
CONTAINER_WRITE = 3
BOOL_WRITE = 4
FIELD_READ = 5
CONTAINER_READ = 6
VALUE_READ = 7
BOOL_READ = 8

def make_helper(v_from, container):

    def helper(func):

        def nested(self, *args, **kwargs):
            assert self.state in (v_from, container), (self.state, v_from, container)
            return func(self, *args, **kwargs)

        return nested

    return helper


writer = make_helper(VALUE_WRITE, CONTAINER_WRITE)
reader = make_helper(VALUE_READ, CONTAINER_READ)

def makeZigZag(n, bits):
    checkIntegerLimits(n, bits)
    return n << 1 ^ n >> bits - 1


def fromZigZag(n):
    return n >> 1 ^ -(n & 1)


def writeVarint(trans, n):
    out = bytearray()
    while True:
        if n & -128 == 0:
            out.append(n)
            break
        else:
            out.append(n & 255 | 128)
            n = n >> 7

    trans.write(bytes(out))


def readVarint(trans):
    result = 0
    shift = 0
    while True:
        x = trans.readAll(1)
        byte = ord(x)
        result |= (byte & 127) << shift
        if byte >> 7 == 0:
            return result
        shift += 7


class CompactType(object):
    STOP = 0
    TRUE = 1
    FALSE = 2
    BYTE = 3
    I16 = 4
    I32 = 5
    I64 = 6
    DOUBLE = 7
    BINARY = 8
    LIST = 9
    SET = 10
    MAP = 11
    STRUCT = 12


CTYPES = {TType.STOP: CompactType.STOP, 
 TType.BOOL: CompactType.TRUE, 
 TType.BYTE: CompactType.BYTE, 
 TType.I16: CompactType.I16, 
 TType.I32: CompactType.I32, 
 TType.I64: CompactType.I64, 
 TType.DOUBLE: CompactType.DOUBLE, 
 TType.STRING: CompactType.BINARY, 
 TType.STRUCT: CompactType.STRUCT, 
 TType.LIST: CompactType.LIST, 
 TType.SET: CompactType.SET, 
 TType.MAP: CompactType.MAP}
TTYPES = {}
for k, v in CTYPES.items():
    TTYPES[v] = k

TTYPES[CompactType.FALSE] = TType.BOOL
del k
del v

class TCompactProtocol(TProtocolBase):
    __doc__ = 'Compact implementation of the Thrift protocol driver.'
    PROTOCOL_ID = 130
    VERSION = 1
    VERSION_MASK = 31
    TYPE_MASK = 224
    TYPE_BITS = 7
    TYPE_SHIFT_AMOUNT = 5

    def __init__(self, trans, string_length_limit=None, container_length_limit=None):
        TProtocolBase.__init__(self, trans)
        self.state = CLEAR
        self._TCompactProtocol__last_fid = 0
        self._TCompactProtocol__bool_fid = None
        self._TCompactProtocol__bool_value = None
        self._TCompactProtocol__structs = []
        self._TCompactProtocol__containers = []
        self.string_length_limit = string_length_limit
        self.container_length_limit = container_length_limit

    def _check_string_length(self, length):
        self._check_length(self.string_length_limit, length)

    def _check_container_length(self, length):
        self._check_length(self.container_length_limit, length)

    def __writeVarint(self, n):
        writeVarint(self.trans, n)

    def writeMessageBegin(self, name, type, seqid):
        assert self.state == CLEAR
        self._TCompactProtocol__writeUByte(self.PROTOCOL_ID)
        self._TCompactProtocol__writeUByte(self.VERSION | type << self.TYPE_SHIFT_AMOUNT)
        self._TCompactProtocol__writeVarint(seqid)
        self._TCompactProtocol__writeBinary(str_to_binary(name))
        self.state = VALUE_WRITE

    def writeMessageEnd(self):
        assert self.state == VALUE_WRITE
        self.state = CLEAR

    def writeStructBegin(self, name):
        assert self.state in (CLEAR, CONTAINER_WRITE, VALUE_WRITE), self.state
        self._TCompactProtocol__structs.append((self.state, self._TCompactProtocol__last_fid))
        self.state = FIELD_WRITE
        self._TCompactProtocol__last_fid = 0

    def writeStructEnd(self):
        assert self.state == FIELD_WRITE
        self.state, self._TCompactProtocol__last_fid = self._TCompactProtocol__structs.pop()

    def writeFieldStop(self):
        self._TCompactProtocol__writeByte(0)

    def __writeFieldHeader(self, type, fid):
        delta = fid - self._TCompactProtocol__last_fid
        if 0 < delta <= 15:
            self._TCompactProtocol__writeUByte(delta << 4 | type)
        else:
            self._TCompactProtocol__writeByte(type)
            self._TCompactProtocol__writeI16(fid)
        self._TCompactProtocol__last_fid = fid

    def writeFieldBegin(self, name, type, fid):
        if not self.state == FIELD_WRITE:
            raise AssertionError(self.state)
        else:
            if type == TType.BOOL:
                self.state = BOOL_WRITE
                self._TCompactProtocol__bool_fid = fid
            else:
                self.state = VALUE_WRITE
                self._TCompactProtocol__writeFieldHeader(CTYPES[type], fid)

    def writeFieldEnd(self):
        assert self.state in (VALUE_WRITE, BOOL_WRITE), self.state
        self.state = FIELD_WRITE

    def __writeUByte(self, byte):
        self.trans.write(pack('!B', byte))

    def __writeByte(self, byte):
        self.trans.write(pack('!b', byte))

    def __writeI16(self, i16):
        self._TCompactProtocol__writeVarint(makeZigZag(i16, 16))

    def __writeSize(self, i32):
        self._TCompactProtocol__writeVarint(i32)

    def writeCollectionBegin(self, etype, size):
        if not self.state in (VALUE_WRITE, CONTAINER_WRITE):
            raise AssertionError(self.state)
        else:
            if size <= 14:
                self._TCompactProtocol__writeUByte(size << 4 | CTYPES[etype])
            else:
                self._TCompactProtocol__writeUByte(240 | CTYPES[etype])
                self._TCompactProtocol__writeSize(size)
        self._TCompactProtocol__containers.append(self.state)
        self.state = CONTAINER_WRITE

    writeSetBegin = writeCollectionBegin
    writeListBegin = writeCollectionBegin

    def writeMapBegin(self, ktype, vtype, size):
        if not self.state in (VALUE_WRITE, CONTAINER_WRITE):
            raise AssertionError(self.state)
        else:
            if size == 0:
                self._TCompactProtocol__writeByte(0)
            else:
                self._TCompactProtocol__writeSize(size)
                self._TCompactProtocol__writeUByte(CTYPES[ktype] << 4 | CTYPES[vtype])
        self._TCompactProtocol__containers.append(self.state)
        self.state = CONTAINER_WRITE

    def writeCollectionEnd(self):
        assert self.state == CONTAINER_WRITE, self.state
        self.state = self._TCompactProtocol__containers.pop()

    writeMapEnd = writeCollectionEnd
    writeSetEnd = writeCollectionEnd
    writeListEnd = writeCollectionEnd

    def writeBool(self, bool):
        if self.state == BOOL_WRITE:
            if bool:
                ctype = CompactType.TRUE
            else:
                ctype = CompactType.FALSE
            self._TCompactProtocol__writeFieldHeader(ctype, self._TCompactProtocol__bool_fid)
        else:
            if self.state == CONTAINER_WRITE:
                if bool:
                    self._TCompactProtocol__writeByte(CompactType.TRUE)
                else:
                    self._TCompactProtocol__writeByte(CompactType.FALSE)
            else:
                raise AssertionError('Invalid state in compact protocol')

    writeByte = writer(_TCompactProtocol__writeByte)
    writeI16 = writer(_TCompactProtocol__writeI16)

    @writer
    def writeI32(self, i32):
        self._TCompactProtocol__writeVarint(makeZigZag(i32, 32))

    @writer
    def writeI64(self, i64):
        self._TCompactProtocol__writeVarint(makeZigZag(i64, 64))

    @writer
    def writeDouble(self, dub):
        self.trans.write(pack('<d', dub))

    def __writeBinary(self, s):
        self._TCompactProtocol__writeSize(len(s))
        self.trans.write(s)

    writeBinary = writer(_TCompactProtocol__writeBinary)

    def readFieldBegin(self):
        assert self.state == FIELD_READ, self.state
        type = self._TCompactProtocol__readUByte()
        if type & 15 == TType.STOP:
            return (None, 0, 0)
        else:
            delta = type >> 4
            if delta == 0:
                fid = self._TCompactProtocol__readI16()
            else:
                fid = self._TCompactProtocol__last_fid + delta
            self._TCompactProtocol__last_fid = fid
            type = type & 15
            if type == CompactType.TRUE:
                self.state = BOOL_READ
                self._TCompactProtocol__bool_value = True
            else:
                if type == CompactType.FALSE:
                    self.state = BOOL_READ
                    self._TCompactProtocol__bool_value = False
                else:
                    self.state = VALUE_READ
            return (
             None, self._TCompactProtocol__getTType(type), fid)

    def readFieldEnd(self):
        assert self.state in (VALUE_READ, BOOL_READ), self.state
        self.state = FIELD_READ

    def __readUByte(self):
        result, = unpack('!B', self.trans.readAll(1))
        return result

    def __readByte(self):
        result, = unpack('!b', self.trans.readAll(1))
        return result

    def __readVarint(self):
        return readVarint(self.trans)

    def __readZigZag(self):
        return fromZigZag(self._TCompactProtocol__readVarint())

    def __readSize(self):
        result = self._TCompactProtocol__readVarint()
        if result < 0:
            raise TProtocolException('Length < 0')
        return result

    def readMessageBegin(self):
        if not self.state == CLEAR:
            raise AssertionError
        else:
            proto_id = self._TCompactProtocol__readUByte()
            if proto_id != self.PROTOCOL_ID:
                raise TProtocolException(TProtocolException.BAD_VERSION, 'Bad protocol id in the message: %d' % proto_id)
            ver_type = self._TCompactProtocol__readUByte()
            type = ver_type >> self.TYPE_SHIFT_AMOUNT & self.TYPE_BITS
            version = ver_type & self.VERSION_MASK
            if version != self.VERSION:
                raise TProtocolException(TProtocolException.BAD_VERSION, 'Bad version: %d (expect %d)' % (version, self.VERSION))
        seqid = self._TCompactProtocol__readVarint()
        name = binary_to_str(self._TCompactProtocol__readBinary())
        return (name, type, seqid)

    def readMessageEnd(self):
        if not self.state == CLEAR:
            raise AssertionError
        elif not len(self._TCompactProtocol__structs) == 0:
            raise AssertionError

    def readStructBegin(self):
        assert self.state in (CLEAR, CONTAINER_READ, VALUE_READ), self.state
        self._TCompactProtocol__structs.append((self.state, self._TCompactProtocol__last_fid))
        self.state = FIELD_READ
        self._TCompactProtocol__last_fid = 0

    def readStructEnd(self):
        assert self.state == FIELD_READ
        self.state, self._TCompactProtocol__last_fid = self._TCompactProtocol__structs.pop()

    def readCollectionBegin(self):
        assert self.state in (VALUE_READ, CONTAINER_READ), self.state
        size_type = self._TCompactProtocol__readUByte()
        size = size_type >> 4
        type = self._TCompactProtocol__getTType(size_type)
        if size == 15:
            size = self._TCompactProtocol__readSize()
        self._check_container_length(size)
        self._TCompactProtocol__containers.append(self.state)
        self.state = CONTAINER_READ
        return (type, size)

    readSetBegin = readCollectionBegin
    readListBegin = readCollectionBegin

    def readMapBegin(self):
        assert self.state in (VALUE_READ, CONTAINER_READ), self.state
        size = self._TCompactProtocol__readSize()
        self._check_container_length(size)
        types = 0
        if size > 0:
            types = self._TCompactProtocol__readUByte()
        vtype = self._TCompactProtocol__getTType(types)
        ktype = self._TCompactProtocol__getTType(types >> 4)
        self._TCompactProtocol__containers.append(self.state)
        self.state = CONTAINER_READ
        return (ktype, vtype, size)

    def readCollectionEnd(self):
        assert self.state == CONTAINER_READ, self.state
        self.state = self._TCompactProtocol__containers.pop()

    readSetEnd = readCollectionEnd
    readListEnd = readCollectionEnd
    readMapEnd = readCollectionEnd

    def readBool(self):
        if self.state == BOOL_READ:
            return self._TCompactProtocol__bool_value == CompactType.TRUE
        if self.state == CONTAINER_READ:
            return self._TCompactProtocol__readByte() == CompactType.TRUE
        raise AssertionError('Invalid state in compact protocol: %d' % self.state)

    readByte = reader(_TCompactProtocol__readByte)
    _TCompactProtocol__readI16 = _TCompactProtocol__readZigZag
    readI16 = reader(_TCompactProtocol__readZigZag)
    readI32 = reader(_TCompactProtocol__readZigZag)
    readI64 = reader(_TCompactProtocol__readZigZag)

    @reader
    def readDouble(self):
        buff = self.trans.readAll(8)
        val, = unpack('<d', buff)
        return val

    def __readBinary(self):
        size = self._TCompactProtocol__readSize()
        self._check_string_length(size)
        return self.trans.readAll(size)

    readBinary = reader(_TCompactProtocol__readBinary)

    def __getTType(self, byte):
        return TTYPES[(byte & 15)]


class TCompactProtocolFactory(object):

    def __init__(self, string_length_limit=None, container_length_limit=None):
        self.string_length_limit = string_length_limit
        self.container_length_limit = container_length_limit

    def getProtocol(self, trans):
        return TCompactProtocol(trans, self.string_length_limit, self.container_length_limit)


class TCompactProtocolAccelerated(TCompactProtocol):
    __doc__ = "C-Accelerated version of TCompactProtocol.\n\n    This class does not override any of TCompactProtocol's methods,\n    but the generated code recognizes it directly and will call into\n    our C module to do the encoding, bypassing this object entirely.\n    We inherit from TCompactProtocol so that the normal TCompactProtocol\n    encoding can happen if the fastbinary module doesn't work for some\n    reason.\n    To disable this behavior, pass fallback=False constructor argument.\n\n    In order to take advantage of the C module, just use\n    TCompactProtocolAccelerated instead of TCompactProtocol.\n    "

    def __init__(self, *args, **kwargs):
        fallback = kwargs.pop('fallback', True)
        (super(TCompactProtocolAccelerated, self).__init__)(*args, **kwargs)
        try:
            from thrift.protocol import fastbinary
        except ImportError:
            if not fallback:
                raise
        else:
            self._fast_decode = fastbinary.decode_compact
            self._fast_encode = fastbinary.encode_compact


class TCompactProtocolAcceleratedFactory(object):

    def __init__(self, string_length_limit=None, container_length_limit=None, fallback=True):
        self.string_length_limit = string_length_limit
        self.container_length_limit = container_length_limit
        self._fallback = fallback

    def getProtocol(self, trans):
        return TCompactProtocolAccelerated(trans,
          string_length_limit=(self.string_length_limit),
          container_length_limit=(self.container_length_limit),
          fallback=(self._fallback))
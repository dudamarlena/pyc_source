# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/umsgpack.py
# Compiled at: 2013-12-10 19:44:48
import struct, collections, sys

class Ext:

    def __init__(self, type, data):
        if not isinstance(type, int) or not (type >= 0 and type <= 127):
            raise TypeError('ext type out of range')
        elif sys.version_info[0] == 3 and not isinstance(data, bytes):
            raise TypeError("ext data is not type 'bytes'")
        elif sys.version_info[0] == 2 and not isinstance(data, str):
            raise TypeError("ext data is not type 'str'")
        self.type = type
        self.data = data

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.type == other.type and self.data == other.data

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        s = 'Ext Object\n'
        s += '   Type: %02x\n' % self.type
        s += '   Data: '
        for i in range(len(self.data)):
            if isinstance(self.data[i], int):
                s += '%02x ' % self.data[i]
            else:
                s += '%02x ' % ord(self.data[i])
            if i == 15:
                break

        if len(self.data) > 16:
            s += '...'
        return s


class PackException(Exception):
    pass


class UnpackException(Exception):
    pass


class UnsupportedTypeException(PackException):
    pass


class InsufficientDataException(UnpackException):
    pass


class InvalidStringException(UnpackException):
    pass


class ReservedCodeException(UnpackException):
    pass


class KeyNotPrimitiveException(UnpackException):
    pass


class KeyDuplicateException(UnpackException):
    pass


packb = None
unpackb = None
compatibility = False

def _pack_integer(x):
    if x < 0:
        if x >= -32:
            return struct.pack('b', x)
        if x >= -2 ** 7:
            return b'\xd0' + struct.pack('b', x)
        if x >= -2 ** 15:
            return b'\xd1' + struct.pack('>h', x)
        if x >= -2 ** 31:
            return b'\xd2' + struct.pack('>i', x)
        if x >= -2 ** 63:
            return b'\xd3' + struct.pack('>q', x)
        raise UnsupportedTypeException('huge signed int')
    else:
        if x <= 127:
            return struct.pack('B', x)
        if x <= 255:
            return b'\xcc' + struct.pack('B', x)
        if x <= 65535:
            return b'\xcd' + struct.pack('>H', x)
        if x <= 4294967295:
            return b'\xce' + struct.pack('>I', x)
        if x <= 18446744073709551615:
            return b'\xcf' + struct.pack('>Q', x)
        raise UnsupportedTypeException('huge unsigned int')


def _pack_nil(x):
    return b'\xc0'


def _pack_boolean(x):
    if x:
        return b'\xc3'
    return b'\xc2'


def _pack_float(x):
    if _float_size == 64:
        return b'\xcb' + struct.pack('>d', x)
    else:
        return b'\xca' + struct.pack('>f', x)


def _pack_string(x):
    if len(x) <= 31:
        return struct.pack('B', 160 | len(x)) + x.encode('utf-8')
    if len(x) <= 255:
        return b'\xd9' + struct.pack('B', len(x)) + x.encode('utf-8')
    if len(x) <= 65535:
        return b'\xda' + struct.pack('>H', len(x)) + x.encode('utf-8')
    if len(x) <= 4294967295:
        return b'\xdb' + struct.pack('>I', len(x)) + x.encode('utf-8')
    raise UnsupportedTypeException('huge string')


def _pack_binary(x):
    if len(x) <= 255:
        return b'\xc4' + struct.pack('B', len(x)) + x
    if len(x) <= 65535:
        return b'\xc5' + struct.pack('>H', len(x)) + x
    if len(x) <= 4294967295:
        return b'\xc6' + struct.pack('>I', len(x)) + x
    raise UnsupportedTypeException('huge binary string')


def _pack_oldspec_raw(x):
    if len(x) <= 31:
        return struct.pack('B', 160 | len(x)) + x
    if len(x) <= 65535:
        return b'\xda' + struct.pack('>H', len(x)) + x
    if len(x) <= 4294967295:
        return b'\xdb' + struct.pack('>I', len(x)) + x
    raise UnsupportedTypeException('huge raw string')


def _pack_ext(x):
    if len(x.data) == 1:
        return b'\xd4' + struct.pack('B', x.type & 255) + x.data
    if len(x.data) == 2:
        return b'\xd5' + struct.pack('B', x.type & 255) + x.data
    if len(x.data) == 4:
        return b'\xd6' + struct.pack('B', x.type & 255) + x.data
    if len(x.data) == 8:
        return b'\xd7' + struct.pack('B', x.type & 255) + x.data
    if len(x.data) == 16:
        return b'\xd8' + struct.pack('B', x.type & 255) + x.data
    if len(x.data) <= 255:
        return b'\xc7' + struct.pack('BB', len(x.data), x.type & 255) + x.data
    if len(x.data) <= 65535:
        return b'\xc8' + struct.pack('>HB', len(x.data), x.type & 255) + x.data
    if len(x.data) <= 4294967295:
        return b'\xc9' + struct.pack('>IB', len(x.data), x.type & 255) + x.data
    raise UnsupportedTypeException('huge ext data')


def _pack_array(x):
    global packb
    if len(x) <= 15:
        s = struct.pack('B', 144 | len(x))
    else:
        if len(x) <= 65535:
            s = b'\xdc' + struct.pack('>H', len(x))
        elif len(x) <= 4294967295:
            s = b'\xdd' + struct.pack('>I', len(x))
        else:
            raise UnsupportedTypeException('huge array')
        for e in x:
            s += packb(e)

    return s


def _pack_map(x):
    if len(x) <= 15:
        s = struct.pack('B', 128 | len(x))
    else:
        if len(x) <= 65535:
            s = b'\xde' + struct.pack('>H', len(x))
        elif len(x) <= 4294967295:
            s = b'\xdf' + struct.pack('>I', len(x))
        else:
            raise UnsupportedTypeException('huge array')
        for k, v in x.items():
            s += packb(k)
            s += packb(v)

    return s


def _packb2(x):
    global compatibility
    if x is None:
        return _pack_nil(x)
    else:
        if isinstance(x, bool):
            return _pack_boolean(x)
        if isinstance(x, int) or isinstance(x, long):
            return _pack_integer(x)
        if isinstance(x, float):
            return _pack_float(x)
        if compatibility and isinstance(x, unicode):
            return _pack_oldspec_raw(bytes(x))
        if compatibility and isinstance(x, bytes):
            return _pack_oldspec_raw(x)
        if isinstance(x, unicode):
            return _pack_string(x)
        if isinstance(x, str):
            return _pack_binary(x)
        if isinstance(x, list) or isinstance(x, tuple):
            return _pack_array(x)
        if isinstance(x, dict):
            return _pack_map(x)
        if isinstance(x, Ext):
            return _pack_ext(x)
        raise UnsupportedTypeException('unsupported type: %s' % str(type(x)))
        return


def _packb3(x):
    if x is None:
        return _pack_nil(x)
    else:
        if isinstance(x, bool):
            return _pack_boolean(x)
        if isinstance(x, int):
            return _pack_integer(x)
        if isinstance(x, float):
            return _pack_float(x)
        if compatibility and isinstance(x, str):
            return _pack_oldspec_raw(x.encode('utf-8'))
        if compatibility and isinstance(x, bytes):
            return _pack_oldspec_raw(x)
        if isinstance(x, str):
            return _pack_string(x)
        if isinstance(x, bytes):
            return _pack_binary(x)
        if isinstance(x, list) or isinstance(x, tuple):
            return _pack_array(x)
        if isinstance(x, dict):
            return _pack_map(x)
        if isinstance(x, Ext):
            return _pack_ext(x)
        raise UnsupportedTypeException('unsupported type: %s' % str(type(x)))
        return


def _unpack_integer(code, read_fn):
    if ord(code) & 224 == 224:
        return struct.unpack('b', code)[0]
    if code == b'\xd0':
        return struct.unpack('b', read_fn(1))[0]
    if code == b'\xd1':
        return struct.unpack('>h', read_fn(2))[0]
    if code == b'\xd2':
        return struct.unpack('>i', read_fn(4))[0]
    if code == b'\xd3':
        return struct.unpack('>q', read_fn(8))[0]
    if ord(code) & 128 == 0:
        return struct.unpack('B', code)[0]
    if code == b'\xcc':
        return struct.unpack('B', read_fn(1))[0]
    if code == b'\xcd':
        return struct.unpack('>H', read_fn(2))[0]
    if code == b'\xce':
        return struct.unpack('>I', read_fn(4))[0]
    if code == b'\xcf':
        return struct.unpack('>Q', read_fn(8))[0]
    raise Exception('logic error, not int: 0x%02x' % ord(code))


def _unpack_reserved(code, read_fn):
    if code == b'\xc1':
        raise ReservedCodeException('encountered reserved code: 0x%02x' % ord(code))
    raise Exception('logic error, not reserved code: 0x%02x' % ord(code))


def _unpack_nil(code, read_fn):
    if code == b'\xc0':
        return
    else:
        raise Exception('logic error, not nil: 0x%02x' % ord(code))
        return


def _unpack_boolean(code, read_fn):
    if code == b'\xc2':
        return False
    if code == b'\xc3':
        return True
    raise Exception('logic error, not boolean: 0x%02x' % ord(code))


def _unpack_float(code, read_fn):
    if code == b'\xca':
        return struct.unpack('>f', read_fn(4))[0]
    if code == b'\xcb':
        return struct.unpack('>d', read_fn(8))[0]
    raise Exception('logic error, not float: 0x%02x' % ord(code))


def _unpack_string(code, read_fn):
    if ord(code) & 224 == 160:
        length = ord(code) & -225
    else:
        if code == b'\xd9':
            length = struct.unpack('B', read_fn(1))[0]
        else:
            if code == b'\xda':
                length = struct.unpack('>H', read_fn(2))[0]
            elif code == b'\xdb':
                length = struct.unpack('>I', read_fn(4))[0]
            else:
                raise Exception('logic error, not string: 0x%02x' % ord(code))
            if compatibility:
                return read_fn(length)
        try:
            return bytes.decode(read_fn(length), 'utf-8')
        except UnicodeDecodeError:
            raise InvalidStringException('unpacked string is not utf-8')


def _unpack_binary(code, read_fn):
    if code == b'\xc4':
        length = struct.unpack('B', read_fn(1))[0]
    elif code == b'\xc5':
        length = struct.unpack('>H', read_fn(2))[0]
    elif code == b'\xc6':
        length = struct.unpack('>I', read_fn(4))[0]
    else:
        raise Exception('logic error, not binary: 0x%02x' % ord(code))
    return read_fn(length)


def _unpack_ext(code, read_fn):
    if code == b'\xd4':
        length = 1
    elif code == b'\xd5':
        length = 2
    elif code == b'\xd6':
        length = 4
    elif code == b'\xd7':
        length = 8
    elif code == b'\xd8':
        length = 16
    elif code == b'\xc7':
        length = struct.unpack('B', read_fn(1))[0]
    elif code == b'\xc8':
        length = struct.unpack('>H', read_fn(2))[0]
    elif code == b'\xc9':
        length = struct.unpack('>I', read_fn(4))[0]
    else:
        raise Exception('logic error, not ext: 0x%02x' % ord(code))
    return Ext(ord(read_fn(1)), read_fn(length))


def _unpack_array(code, read_fn):
    if ord(code) & 240 == 144:
        length = ord(code) & -241
    elif code == b'\xdc':
        length = struct.unpack('>H', read_fn(2))[0]
    elif code == b'\xdd':
        length = struct.unpack('>I', read_fn(4))[0]
    else:
        raise Exception('logic error, not array: 0x%02x' % ord(code))
    return [ _unpackb(read_fn) for i in range(length) ]


def _unpack_map(code, read_fn):
    if ord(code) & 240 == 128:
        length = ord(code) & -241
    else:
        if code == b'\xde':
            length = struct.unpack('>H', read_fn(2))[0]
        elif code == b'\xdf':
            length = struct.unpack('>I', read_fn(4))[0]
        else:
            raise Exception('logic error, not map: 0x%02x' % ord(code))
        d = {}
        for i in range(length):
            k = _unpackb(read_fn)
            if not isinstance(k, collections.Hashable):
                raise KeyNotPrimitiveException('encountered non-primitive key type: %s' % str(type(k)))
            elif k in d:
                raise KeyDuplicateException('encountered duplicate key: %s, %s' % (str(k), str(type(k))))
            v = _unpackb(read_fn)
            d[k] = v

    return d


def _byte_reader(s):
    i = [
     0]

    def read_fn(n):
        if i[0] + n > len(s):
            raise InsufficientDataException()
        substring = s[i[0]:i[0] + n]
        i[0] += n
        return substring

    return read_fn


def _unpackb(read_fn):
    code = read_fn(1)
    return _unpack_dispatch_table[code](code, read_fn)


def _unpackb2(s):
    if not isinstance(s, str):
        raise TypeError("packed data is not type 'str'")
    read_fn = _byte_reader(s)
    return _unpackb(read_fn)


def _unpackb3(s):
    if not isinstance(s, bytes):
        raise TypeError("packed data is not type 'bytes'")
    read_fn = _byte_reader(s)
    return _unpackb(read_fn)


def __init():
    global _float_size
    global _unpack_dispatch_table
    global compatibility
    global packb
    global unpackb
    compatibility = False
    if sys.float_info.mant_dig == 53:
        _float_size = 64
    else:
        _float_size = 32
    if sys.version_info[0] == 3:
        packb = _packb3
        unpackb = _unpackb3
    else:
        packb = _packb2
        unpackb = _unpackb2
    _unpack_dispatch_table = {}
    for code in range(0, 128):
        _unpack_dispatch_table[struct.pack('B', code)] = _unpack_integer

    for code in range(128, 144):
        _unpack_dispatch_table[struct.pack('B', code)] = _unpack_map

    for code in range(144, 160):
        _unpack_dispatch_table[struct.pack('B', code)] = _unpack_array

    for code in range(160, 192):
        _unpack_dispatch_table[struct.pack('B', code)] = _unpack_string

    _unpack_dispatch_table[b'\xc0'] = _unpack_nil
    _unpack_dispatch_table[b'\xc1'] = _unpack_reserved
    _unpack_dispatch_table[b'\xc2'] = _unpack_boolean
    _unpack_dispatch_table[b'\xc3'] = _unpack_boolean
    for code in range(196, 199):
        _unpack_dispatch_table[struct.pack('B', code)] = _unpack_binary

    for code in range(199, 202):
        _unpack_dispatch_table[struct.pack('B', code)] = _unpack_ext

    _unpack_dispatch_table[b'\xca'] = _unpack_float
    _unpack_dispatch_table[b'\xcb'] = _unpack_float
    for code in range(204, 208):
        _unpack_dispatch_table[struct.pack('B', code)] = _unpack_integer

    for code in range(208, 212):
        _unpack_dispatch_table[struct.pack('B', code)] = _unpack_integer

    for code in range(212, 217):
        _unpack_dispatch_table[struct.pack('B', code)] = _unpack_ext

    for code in range(217, 220):
        _unpack_dispatch_table[struct.pack('B', code)] = _unpack_string

    _unpack_dispatch_table[b'\xdc'] = _unpack_array
    _unpack_dispatch_table[b'\xdd'] = _unpack_array
    _unpack_dispatch_table[b'\xde'] = _unpack_map
    _unpack_dispatch_table[b'\xdf'] = _unpack_map
    for code in range(224, 256):
        _unpack_dispatch_table[struct.pack('B', code)] = _unpack_integer


__init()
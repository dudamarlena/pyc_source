# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/libesedb/esetypes.py
# Compiled at: 2014-07-11 17:28:23
import struct, logging
log = logging.getLogger('libesedb.types')

class Identifiers(object):

    class __metaclass__(type):

        def __init__(cls, name, dct, bases):
            type.__init__(cls, name, dct, bases)
            v2n = {}
            n2v = {}
            for k, v in cls.__dict__.iteritems():
                if not k.startswith('_') and type(v) is int:
                    v2n[v] = k
                    n2v[k] = v

            cls.n2v = n2v
            cls.v2n = v2n

        def __getitem__(self, attr):
            return self.v2n.get(attr, str(attr))

        def flag(self, flag):
            s = [ k for k, v in self.n2v.iteritems() if flag & v != 0 ]
            return ('|').join(s)


class ColumnType(Identifiers):
    NULL = 0
    BOOLEAN = 1
    INTEGER_8BIT_UNSIGNED = 2
    INTEGER_16BIT_SIGNED = 3
    INTEGER_32BIT_SIGNED = 4
    CURRENCY = 5
    FLOAT_32BIT = 6
    DOUBLE_64BIT = 7
    DATE_TIME = 8
    BINARY_DATA = 9
    TEXT = 10
    LARGE_BINARY_DATA = 11
    LARGE_TEXT = 12
    SUPER_LARGE_VALUE = 13
    INTEGER_32BIT_UNSIGNED = 14
    INTEGER_64BIT_SIGNED = 15
    GUID = 16
    INTEGER_16BIT_UNSIGNED = 17


class ValueFlags(Identifiers):
    VARIABLE_SIZE = 1
    COMPRESSED = 2
    LONG_VALUE = 4
    MULTI_VALUE = 8
    FLAG_0x10 = 16


def decode_guid(s):
    part1 = '%08x-%04x-%04x-' % struct.unpack('<IHH', s[:8])
    part2 = '%04x-%08x%04x' % struct.unpack('>HIH', s[8:])
    return part1 + part2


def decode_maybe_utf16(val):
    try:
        return val.decode('utf16')
    except UnicodeDecodeError:
        return val


converters = {ColumnType.GUID: lambda x: decode_guid(x), 
   ColumnType.INTEGER_8BIT_UNSIGNED: lambda x: struct.unpack('<B', x)[0], 
   ColumnType.INTEGER_16BIT_SIGNED: lambda x: struct.unpack('<h', x)[0], 
   ColumnType.INTEGER_16BIT_UNSIGNED: lambda x: struct.unpack('<H', x)[0], 
   ColumnType.INTEGER_32BIT_SIGNED: lambda x: struct.unpack('<i', x)[0], 
   ColumnType.INTEGER_32BIT_UNSIGNED: lambda x: struct.unpack('<I', x)[0], 
   ColumnType.INTEGER_64BIT_SIGNED: lambda x: struct.unpack('<q', x)[0], 
   ColumnType.CURRENCY: lambda x: struct.unpack('<Q', x)[0], 
   ColumnType.TEXT: decode_maybe_utf16, 
   ColumnType.LARGE_TEXT: decode_maybe_utf16}

def native_type(typ, val):
    if typ in converters:
        return converters[typ](val)
    return val


def multi_native_type(flags, typ, val):
    if flags & ValueFlags.FLAG_0x10 == 0:
        try:
            first, = struct.unpack_from('<H', val)
            first &= 32767
            ofsb = list(struct.unpack_from('<%iH' % (first / 2), val))
            ofsb = [ x & 32767 for x in ofsb ]
        except Exception as e:
            log.warning('ERROR decoding multivalue header: %s' % e)
            return [val]

    else:
        length = ord(val[0])
        ofsb = range(1, len(val), length)
    ofse = ofsb[1:] + [len(val)]
    try:
        sval = [ val[start:end] for start, end in zip(ofsb, ofse) ]
    except Exception as e:
        log.warning('ERROR splitting multivalue: %s' % e)
        return [val]

    if typ in converters:
        try:
            sval = map(converters[typ], sval)
        except Exception as e:
            log.warning('ERROR converting multivalue: %s' % e)

    return sval
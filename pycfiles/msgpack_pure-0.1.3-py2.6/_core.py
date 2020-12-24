# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/msgpack_pure/_core.py
# Compiled at: 2011-06-28 01:26:49
import struct, mmap
_NIL = 192
_TRUE = 195
_FALSE = 194
_UINT8 = 204
_UINT16 = 205
_UINT32 = 206
_UINT64 = 207
_INT8 = 208
_INT16 = 209
_INT32 = 210
_INT64 = 211
_FLOAT = 202
_DOUBLE = 203
_FIX_RAW = 160
_RAW16 = 218
_RAW32 = 219
_FIX_ARY = 144
_ARY16 = 220
_ARY32 = 221
_FIX_MAP = 128
_MAP16 = 222
_MAP32 = 223
_INT8_MAX = 127
_INT8_MIN = -_INT8_MAX - 1
_INT16_MAX = 32767
_INT16_MIN = -_INT16_MAX - 1
_INT32_MAX = 2147483647
_INT32_MIN = -_INT32_MAX - 1
_INT64_MAX = 9223372036854775807
_INT64_MIN = -_INT64_MAX - 1
_UINT8_MAX = 255
_UINT16_MAX = 65535
_UINT32_MAX = 4294967295
_UINT64_MAX = 18446744073709551615

def packs(obj, **kwargs):
    if kwargs.get('default'):
        obj = kwargs['default'](obj)
    if obj == None:
        return chr(_NIL)
    else:
        if isinstance(obj, bool) and obj:
            return chr(_TRUE)
        if isinstance(obj, bool) and obj == False:
            return chr(_FALSE)
        if isinstance(obj, int) or isinstance(obj, long):
            if 0 <= obj and obj <= 127:
                return struct.pack('B', obj)
            if -32 <= obj and obj <= 0:
                return struct.pack('b', obj)
            if 0 <= obj <= _UINT8_MAX:
                return struct.pack('BB', _UINT8, obj)
            if _INT8_MIN <= obj and obj <= _INT8_MAX:
                return struct.pack('>Bb', _INT8, obj)
            if 0 <= obj <= _UINT16_MAX:
                return struct.pack('>BH', _UINT16, obj)
            if _INT16_MIN <= obj and obj <= _INT16_MAX:
                return struct.pack('>Bh', _INT16, obj)
            if _INT32_MIN <= obj and obj <= _INT32_MAX:
                return struct.pack('>Bi', _INT32, obj)
            if 0 <= obj <= _UINT32_MAX:
                return struct.pack('>BI', _UINT32, obj)
            if _INT64_MIN <= obj and obj <= _INT64_MAX:
                return struct.pack('>Bq', _INT64, obj)
            if 0 <= obj <= _UINT64_MAX:
                return struct.pack('>BQ', _UINT64, obj)
            raise RuntimeError('Integer value out of range')
        if isinstance(obj, str) or isinstance(obj, unicode):
            if isinstance(obj, unicode):
                obj = obj.encode('utf-8')
            nbytes = len(obj)
            if nbytes <= 31:
                mark = chr(_FIX_RAW + nbytes)
                obj = mark + obj
                return struct.pack('%ds' % len(obj), obj)
            if nbytes <= 65535:
                return struct.pack('>BH%ds' % nbytes, _RAW16, nbytes, obj)
            if nbytes <= 4294967295:
                return struct.pack('>BI%ds' % nbytes, _RAW32, nbytes, obj)
        if isinstance(obj, float):
            return struct.pack('>Bd', _DOUBLE, obj)
        if isinstance(obj, list) or isinstance(obj, tuple):
            packed = ''
            sz = len(obj)
            if sz <= 15:
                packed += chr(_FIX_ARY + (sz & 15))
                for i in range(sz):
                    packed += packs(obj[i], **kwargs)

            elif sz <= 65535:
                packed += chr(_ARY16)
                packed += struct.pack('>H', sz)
                for i in range(sz):
                    packed += packs(obj[i], **kwargs)

            elif sz <= 4294967295:
                packed += chr(_ARY32)
                packed += struct.pack('>I', sz)
                for i in range(sz):
                    packed += packs(obj[i], **kwargs)

            return packed
        if isinstance(obj, dict):
            sz = len(obj)
            packed = ''
            if sz <= 15:
                packed += chr(_FIX_MAP + sz)
            elif sz <= 65535:
                packed += struct.pack('>BH', _MAP16, sz)
            elif sz <= 4294967295:
                packed += struct.pack('>BI', _MAP32, sz)
            for (k, v) in obj.iteritems():
                packed += packs(k, **kwargs)
                packed += packs(v, **kwargs)

            return packed
        raise TypeError()
        return


class Unpacker:

    def __init__(self, **kwargs):
        self.default_hook = kwargs.get('default')
        self.object_hook = kwargs.get('object_hook')
        self.list_hook = kwargs.get('list_hook')
        if self.list_hook and not callable(self.list_hook):
            raise TypeError('list_hook must be a callable.')
        if self.object_hook and not callable(self.object_hook):
            raise TypeError('object_hook must be a callable.')
        if self.default_hook and not callable(self.default_hook):
            raise TypeError('default_hook must be a callable.')

    def apply_hook(self, obj, **kwargs):
        if self.list_hook and (isinstance(obj, list) or isinstance(obj, tuple)):
            obj = self.list_hook(obj)
        elif self.object_hook and isinstance(obj, dict):
            obj = self.object_hook(obj)
        elif self.default_hook:
            obj = self.default_hook(obj)
        return obj

    def unpacks(self, packed):
        if packed is None or len(packed) == 0:
            return
        else:
            mp = mmap.mmap(-1, len(packed))
            mp.write(packed)
            mp.seek(0)
            obj = self.read_obj(mp)
            return obj

    def read_obj(self, mp):
        try:
            b = ord(mp.read_byte())
        except ValueError, e:
            return
        else:
            if b & 128 == 0:
                obj = b
            elif b & 224 == 224:
                obj = struct.unpack('b', chr(b))[0]
            elif b == _UINT8:
                obj = struct.unpack('B', mp.read_byte())[0]
            elif b == _INT8:
                obj = struct.unpack('b', mp.read_byte())[0]
            elif b == _UINT16:
                obj = struct.unpack('>H', mp.read(2))[0]
            elif b == _INT16:
                obj = struct.unpack('>h', mp.read(2))[0]
            elif b == _UINT32:
                obj = struct.unpack('>I', mp.read(4))[0]
            elif b == _INT32:
                obj = struct.unpack('>i', mp.read(4))[0]
            elif b == _UINT64:
                obj = struct.unpack('>Q', mp.read(8))[0]
            elif b == _INT64:
                obj = struct.unpack('>q', mp.read(8))[0]
            elif b == _FLOAT:
                obj = struct.unpack('>f', mp.read(4))[0]
            elif b == _DOUBLE:
                obj = struct.unpack('>d', mp.read(8))[0]
            elif b == _NIL:
                obj = None
            elif b == _TRUE:
                obj = True
            elif b == _FALSE:
                obj = False
            elif b & 224 == _FIX_RAW:
                nbytes = b & 31
                obj = struct.unpack('%ds' % nbytes, mp.read(nbytes))[0]
            elif b == _RAW16:
                (nbytes,) = struct.unpack('>H', mp.read(2))
                obj = struct.unpack('%ds' % nbytes, mp.read(nbytes))[0]
            elif b == _RAW32:
                nbytes = struct.unpack('>I', mp.read(4))[0]
                obj = struct.unpack('%ds' % nbytes, mp.read(nbytes))[0]
            elif b & 240 == _FIX_ARY:
                sz = b & 15
                obj = self.read_list_body(mp, sz)
            elif b == _ARY16:
                sz = struct.unpack('>H', mp.read(2))[0]
                obj = self.read_list_body(mp, sz)
            elif b == _ARY32:
                sz = struct.unpack('>I', mp.read(4))[0]
                obj = self.read_list_body(mp, sz)
            elif b & 240 == _FIX_MAP:
                sz = b & 15
                obj = self.read_map_body(mp, sz)
            elif b == _MAP16:
                sz = struct.unpack('>H', mp.read(2))[0]
                obj = self.read_map_body(mp, sz)
            elif b == _MAP32:
                sz = struct.unpack('>I', mp.read(4))[0]
                obj = self.read_map_body(mp, sz)
            else:
                raise RuntimeError('Unknown object header: 0x%x' % b)

        return self.apply_hook(obj)

    def read_list_body(self, mp, sz):
        obj = []
        for i in range(sz):
            o = self.read_obj(mp)
            o = self.apply_hook(o)
            obj.append(o)

        obj = tuple(obj)
        return self.apply_hook(obj)

    def read_map_body(self, mp, sz):
        obj = {}
        for i in range(sz):
            k = self.read_obj(mp)
            v = self.read_obj(mp)
            k = self.apply_hook(k)
            v = self.apply_hook(v)
            obj[k] = v

        return self.apply_hook(obj)


def unpacks(packed, **kwargs):
    return Unpacker(**kwargs).unpacks(packed)


unpack = unpackb = unpacks
pack = packb = packs
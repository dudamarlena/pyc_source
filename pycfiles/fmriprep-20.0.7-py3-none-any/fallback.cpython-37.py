# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_vendor/msgpack/fallback.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 37133 bytes
"""Fallback pure Python implementation of msgpack"""
from datetime import datetime as _DateTime
import sys, struct
PY2 = sys.version_info[0] == 2
if PY2:
    int_types = (
     int, long)

    def dict_iteritems(d):
        return d.iteritems()


else:
    int_types = int
    unicode = str
    xrange = range

    def dict_iteritems(d):
        return d.items()


if sys.version_info < (3, 5):
    RecursionError = RuntimeError

    def _is_recursionerror(e):
        return len(e.args) == 1 and isinstance(e.args[0], str) and e.args[0].startswith('maximum recursion depth exceeded')


else:

    def _is_recursionerror(e):
        return True


if hasattr(sys, 'pypy_version_info'):
    from __pypy__ import newlist_hint
    try:
        import __pypy__.builders as StringBuilder
    except ImportError:
        from __pypy__.builders import StringBuilder

    USING_STRINGBUILDER = True

    class StringIO(object):

        def __init__(self, s=b''):
            if s:
                self.builder = StringBuilder(len(s))
                self.builder.append(s)
            else:
                self.builder = StringBuilder()

        def write(self, s):
            if isinstance(s, memoryview):
                s = s.tobytes()
            else:
                if isinstance(s, bytearray):
                    s = bytes(s)
            self.builder.append(s)

        def getvalue(self):
            return self.builder.build()


else:
    USING_STRINGBUILDER = False
    from io import BytesIO as StringIO
    newlist_hint = lambda size: []
from .exceptions import BufferFull, OutOfData, ExtraData, FormatError, StackError
from .ext import ExtType, Timestamp
EX_SKIP = 0
EX_CONSTRUCT = 1
EX_READ_ARRAY_HEADER = 2
EX_READ_MAP_HEADER = 3
TYPE_IMMEDIATE = 0
TYPE_ARRAY = 1
TYPE_MAP = 2
TYPE_RAW = 3
TYPE_BIN = 4
TYPE_EXT = 5
DEFAULT_RECURSE_LIMIT = 511

def _check_type_strict(obj, t, type=type, tuple=tuple):
    if type(t) is tuple:
        return type(obj) in t
    return type(obj) is t


def _get_data_from_buffer(obj):
    view = memoryview(obj)
    if view.itemsize != 1:
        raise ValueError('cannot unpack from multi-byte object')
    return view


def unpackb(packed, **kwargs):
    """
    Unpack an object from `packed`.

    Raises ``ExtraData`` when *packed* contains extra bytes.
    Raises ``ValueError`` when *packed* is incomplete.
    Raises ``FormatError`` when *packed* is not valid msgpack.
    Raises ``StackError`` when *packed* contains too nested.
    Other exceptions can be raised during unpacking.

    See :class:`Unpacker` for options.
    """
    unpacker = Unpacker(None, max_buffer_size=len(packed), **kwargs)
    unpacker.feed(packed)
    try:
        ret = unpacker._unpack()
    except OutOfData:
        raise ValueError('Unpack failed: incomplete input')
    except RecursionError as e:
        try:
            if _is_recursionerror(e):
                raise StackError
            raise
        finally:
            e = None
            del e

    if unpacker._got_extradata():
        raise ExtraData(ret, unpacker._get_extradata())
    return ret


if sys.version_info < (2, 7, 6):

    def _unpack_from(f, b, o=0):
        """Explicit type cast for legacy struct.unpack_from"""
        return struct.unpack_from(f, bytes(b), o)


else:
    _unpack_from = struct.unpack_from

class Unpacker(object):
    __doc__ = "Streaming unpacker.\n\n    Arguments:\n\n    :param file_like:\n        File-like object having `.read(n)` method.\n        If specified, unpacker reads serialized data from it and :meth:`feed()` is not usable.\n\n    :param int read_size:\n        Used as `file_like.read(read_size)`. (default: `min(16*1024, max_buffer_size)`)\n\n    :param bool use_list:\n        If true, unpack msgpack array to Python list.\n        Otherwise, unpack to Python tuple. (default: True)\n\n    :param bool raw:\n        If true, unpack msgpack raw to Python bytes.\n        Otherwise, unpack to Python str by decoding with UTF-8 encoding (default).\n\n    :param int timestamp:\n        Control how timestamp type is unpacked:\n\n            0 - Timestamp\n            1 - float  (Seconds from the EPOCH)\n            2 - int  (Nanoseconds from the EPOCH)\n            3 - datetime.datetime  (UTC).  Python 2 is not supported.\n\n    :param bool strict_map_key:\n        If true (default), only str or bytes are accepted for map (dict) keys.\n\n    :param callable object_hook:\n        When specified, it should be callable.\n        Unpacker calls it with a dict argument after unpacking msgpack map.\n        (See also simplejson)\n\n    :param callable object_pairs_hook:\n        When specified, it should be callable.\n        Unpacker calls it with a list of key-value pairs after unpacking msgpack map.\n        (See also simplejson)\n\n    :param str unicode_errors:\n        The error handler for decoding unicode. (default: 'strict')\n        This option should be used only when you have msgpack data which\n        contains invalid UTF-8 string.\n\n    :param int max_buffer_size:\n        Limits size of data waiting unpacked.  0 means 2**32-1.\n        The default value is 100*1024*1024 (100MiB).\n        Raises `BufferFull` exception when it is insufficient.\n        You should set this parameter when unpacking data from untrusted source.\n\n    :param int max_str_len:\n        Deprecated, use *max_buffer_size* instead.\n        Limits max length of str. (default: max_buffer_size)\n\n    :param int max_bin_len:\n        Deprecated, use *max_buffer_size* instead.\n        Limits max length of bin. (default: max_buffer_size)\n\n    :param int max_array_len:\n        Limits max length of array.\n        (default: max_buffer_size)\n\n    :param int max_map_len:\n        Limits max length of map.\n        (default: max_buffer_size//2)\n\n    :param int max_ext_len:\n        Deprecated, use *max_buffer_size* instead.\n        Limits max size of ext type.  (default: max_buffer_size)\n\n    Example of streaming deserialize from file-like object::\n\n        unpacker = Unpacker(file_like)\n        for o in unpacker:\n            process(o)\n\n    Example of streaming deserialize from socket::\n\n        unpacker = Unpacker(max_buffer_size)\n        while True:\n            buf = sock.recv(1024**2)\n            if not buf:\n                break\n            unpacker.feed(buf)\n            for o in unpacker:\n                process(o)\n\n    Raises ``ExtraData`` when *packed* contains extra bytes.\n    Raises ``OutOfData`` when *packed* is incomplete.\n    Raises ``FormatError`` when *packed* is not valid msgpack.\n    Raises ``StackError`` when *packed* contains too nested.\n    Other exceptions can be raised during unpacking.\n    "

    def __init__(self, file_like=None, read_size=0, use_list=True, raw=False, timestamp=0, strict_map_key=True, object_hook=None, object_pairs_hook=None, list_hook=None, unicode_errors=None, max_buffer_size=104857600, ext_hook=ExtType, max_str_len=-1, max_bin_len=-1, max_array_len=-1, max_map_len=-1, max_ext_len=-1):
        if unicode_errors is None:
            unicode_errors = 'strict'
        else:
            if file_like is None:
                self._feeding = True
            else:
                if not callable(file_like.read):
                    raise TypeError('`file_like.read` must be callable')
                self.file_like = file_like
                self._feeding = False
            self._buffer = bytearray()
            self._buff_i = 0
            self._buf_checkpoint = 0
            if not max_buffer_size:
                max_buffer_size = 2147483647
            if max_str_len == -1:
                max_str_len = max_buffer_size
            if max_bin_len == -1:
                max_bin_len = max_buffer_size
            if max_array_len == -1:
                max_array_len = max_buffer_size
            if max_map_len == -1:
                max_map_len = max_buffer_size // 2
            if max_ext_len == -1:
                max_ext_len = max_buffer_size
            self._max_buffer_size = max_buffer_size
            if read_size > self._max_buffer_size:
                raise ValueError('read_size must be smaller than max_buffer_size')
            self._read_size = read_size or min(self._max_buffer_size, 16384)
            self._raw = bool(raw)
            self._strict_map_key = bool(strict_map_key)
            self._unicode_errors = unicode_errors
            self._use_list = use_list
            if not 0 <= timestamp <= 3:
                raise ValueError('timestamp must be 0..3')
            self._timestamp = timestamp
            self._list_hook = list_hook
            self._object_hook = object_hook
            self._object_pairs_hook = object_pairs_hook
            self._ext_hook = ext_hook
            self._max_str_len = max_str_len
            self._max_bin_len = max_bin_len
            self._max_array_len = max_array_len
            self._max_map_len = max_map_len
            self._max_ext_len = max_ext_len
            self._stream_offset = 0
            if list_hook is not None and not callable(list_hook):
                raise TypeError('`list_hook` is not callable')
            if object_hook is not None and not callable(object_hook):
                raise TypeError('`object_hook` is not callable')
            if object_pairs_hook is not None and not callable(object_pairs_hook):
                raise TypeError('`object_pairs_hook` is not callable')
            if object_hook is not None:
                if object_pairs_hook is not None:
                    raise TypeError('object_pairs_hook and object_hook are mutually exclusive')
            assert callable(ext_hook), '`ext_hook` is not callable'

    def feed(self, next_bytes):
        assert self._feeding
        view = _get_data_from_buffer(next_bytes)
        if len(self._buffer) - self._buff_i + len(view) > self._max_buffer_size:
            raise BufferFull
        if self._buf_checkpoint > 0:
            del self._buffer[:self._buf_checkpoint]
            self._buff_i -= self._buf_checkpoint
            self._buf_checkpoint = 0
        self._buffer.extend(view)

    def _consume(self):
        """ Gets rid of the used parts of the buffer. """
        self._stream_offset += self._buff_i - self._buf_checkpoint
        self._buf_checkpoint = self._buff_i

    def _got_extradata(self):
        return self._buff_i < len(self._buffer)

    def _get_extradata(self):
        return self._buffer[self._buff_i:]

    def read_bytes(self, n):
        ret = self._read(n)
        self._consume()
        return ret

    def _read(self, n):
        self._reserve(n)
        i = self._buff_i
        self._buff_i = i + n
        return self._buffer[i:i + n]

    def _reserve(self, n):
        remain_bytes = len(self._buffer) - self._buff_i - n
        if remain_bytes >= 0:
            return
        if self._feeding:
            self._buff_i = self._buf_checkpoint
            raise OutOfData
        if self._buf_checkpoint > 0:
            del self._buffer[:self._buf_checkpoint]
            self._buff_i -= self._buf_checkpoint
            self._buf_checkpoint = 0
        remain_bytes = -remain_bytes
        while remain_bytes > 0:
            to_read_bytes = max(self._read_size, remain_bytes)
            read_data = self.file_like.read(to_read_bytes)
            if not read_data:
                break
            assert isinstance(read_data, bytes)
            self._buffer += read_data
            remain_bytes -= len(read_data)

        if len(self._buffer) < n + self._buff_i:
            self._buff_i = 0
            raise OutOfData

    def _read_header(self, execute=EX_CONSTRUCT):
        typ = TYPE_IMMEDIATE
        n = 0
        obj = None
        self._reserve(1)
        b = self._buffer[self._buff_i]
        self._buff_i += 1
        if b & 128 == 0:
            obj = b
        else:
            if b & 224 == 224:
                obj = -1 - (b ^ 255)
            else:
                if b & 224 == 160:
                    n = b & 31
                    typ = TYPE_RAW
                    if n > self._max_str_len:
                        raise ValueError('%s exceeds max_str_len(%s)', n, self._max_str_len)
                    obj = self._read(n)
                else:
                    if b & 240 == 144:
                        n = b & 15
                        typ = TYPE_ARRAY
                        if n > self._max_array_len:
                            raise ValueError('%s exceeds max_array_len(%s)', n, self._max_array_len)
                    else:
                        if b & 240 == 128:
                            n = b & 15
                            typ = TYPE_MAP
                            if n > self._max_map_len:
                                raise ValueError('%s exceeds max_map_len(%s)', n, self._max_map_len)
                        elif b == 192:
                            obj = None
                        else:
                            if b == 194:
                                obj = False
                            else:
                                if b == 195:
                                    obj = True
                                else:
                                    if b == 196:
                                        typ = TYPE_BIN
                                        self._reserve(1)
                                        n = self._buffer[self._buff_i]
                                        self._buff_i += 1
                                        if n > self._max_bin_len:
                                            raise ValueError('%s exceeds max_bin_len(%s)' % (n, self._max_bin_len))
                                        obj = self._read(n)
                                    else:
                                        if b == 197:
                                            typ = TYPE_BIN
                                            self._reserve(2)
                                            n = _unpack_from('>H', self._buffer, self._buff_i)[0]
                                            self._buff_i += 2
                                            if n > self._max_bin_len:
                                                raise ValueError('%s exceeds max_bin_len(%s)' % (n, self._max_bin_len))
                                            obj = self._read(n)
                                        else:
                                            if b == 198:
                                                typ = TYPE_BIN
                                                self._reserve(4)
                                                n = _unpack_from('>I', self._buffer, self._buff_i)[0]
                                                self._buff_i += 4
                                                if n > self._max_bin_len:
                                                    raise ValueError('%s exceeds max_bin_len(%s)' % (n, self._max_bin_len))
                                                obj = self._read(n)
                                            else:
                                                if b == 199:
                                                    typ = TYPE_EXT
                                                    self._reserve(2)
                                                    L, n = _unpack_from('Bb', self._buffer, self._buff_i)
                                                    self._buff_i += 2
                                                    if L > self._max_ext_len:
                                                        raise ValueError('%s exceeds max_ext_len(%s)' % (L, self._max_ext_len))
                                                    obj = self._read(L)
                                                else:
                                                    if b == 200:
                                                        typ = TYPE_EXT
                                                        self._reserve(3)
                                                        L, n = _unpack_from('>Hb', self._buffer, self._buff_i)
                                                        self._buff_i += 3
                                                        if L > self._max_ext_len:
                                                            raise ValueError('%s exceeds max_ext_len(%s)' % (L, self._max_ext_len))
                                                        obj = self._read(L)
                                                    else:
                                                        if b == 201:
                                                            typ = TYPE_EXT
                                                            self._reserve(5)
                                                            L, n = _unpack_from('>Ib', self._buffer, self._buff_i)
                                                            self._buff_i += 5
                                                            if L > self._max_ext_len:
                                                                raise ValueError('%s exceeds max_ext_len(%s)' % (L, self._max_ext_len))
                                                            obj = self._read(L)
                                                        else:
                                                            if b == 202:
                                                                self._reserve(4)
                                                                obj = _unpack_from('>f', self._buffer, self._buff_i)[0]
                                                                self._buff_i += 4
                                                            else:
                                                                if b == 203:
                                                                    self._reserve(8)
                                                                    obj = _unpack_from('>d', self._buffer, self._buff_i)[0]
                                                                    self._buff_i += 8
                                                                else:
                                                                    if b == 204:
                                                                        self._reserve(1)
                                                                        obj = self._buffer[self._buff_i]
                                                                        self._buff_i += 1
                                                                    else:
                                                                        if b == 205:
                                                                            self._reserve(2)
                                                                            obj = _unpack_from('>H', self._buffer, self._buff_i)[0]
                                                                            self._buff_i += 2
                                                                        else:
                                                                            if b == 206:
                                                                                self._reserve(4)
                                                                                obj = _unpack_from('>I', self._buffer, self._buff_i)[0]
                                                                                self._buff_i += 4
                                                                            else:
                                                                                if b == 207:
                                                                                    self._reserve(8)
                                                                                    obj = _unpack_from('>Q', self._buffer, self._buff_i)[0]
                                                                                    self._buff_i += 8
                                                                                else:
                                                                                    if b == 208:
                                                                                        self._reserve(1)
                                                                                        obj = _unpack_from('b', self._buffer, self._buff_i)[0]
                                                                                        self._buff_i += 1
                                                                                    else:
                                                                                        if b == 209:
                                                                                            self._reserve(2)
                                                                                            obj = _unpack_from('>h', self._buffer, self._buff_i)[0]
                                                                                            self._buff_i += 2
                                                                                        else:
                                                                                            if b == 210:
                                                                                                self._reserve(4)
                                                                                                obj = _unpack_from('>i', self._buffer, self._buff_i)[0]
                                                                                                self._buff_i += 4
                                                                                            else:
                                                                                                if b == 211:
                                                                                                    self._reserve(8)
                                                                                                    obj = _unpack_from('>q', self._buffer, self._buff_i)[0]
                                                                                                    self._buff_i += 8
                                                                                                else:
                                                                                                    if b == 212:
                                                                                                        typ = TYPE_EXT
                                                                                                        if self._max_ext_len < 1:
                                                                                                            raise ValueError('%s exceeds max_ext_len(%s)' % (1, self._max_ext_len))
                                                                                                        self._reserve(2)
                                                                                                        n, obj = _unpack_from('b1s', self._buffer, self._buff_i)
                                                                                                        self._buff_i += 2
                                                                                                    else:
                                                                                                        if b == 213:
                                                                                                            typ = TYPE_EXT
                                                                                                            if self._max_ext_len < 2:
                                                                                                                raise ValueError('%s exceeds max_ext_len(%s)' % (2, self._max_ext_len))
                                                                                                            self._reserve(3)
                                                                                                            n, obj = _unpack_from('b2s', self._buffer, self._buff_i)
                                                                                                            self._buff_i += 3
                                                                                                        else:
                                                                                                            if b == 214:
                                                                                                                typ = TYPE_EXT
                                                                                                                if self._max_ext_len < 4:
                                                                                                                    raise ValueError('%s exceeds max_ext_len(%s)' % (4, self._max_ext_len))
                                                                                                                self._reserve(5)
                                                                                                                n, obj = _unpack_from('b4s', self._buffer, self._buff_i)
                                                                                                                self._buff_i += 5
                                                                                                            else:
                                                                                                                if b == 215:
                                                                                                                    typ = TYPE_EXT
                                                                                                                    if self._max_ext_len < 8:
                                                                                                                        raise ValueError('%s exceeds max_ext_len(%s)' % (8, self._max_ext_len))
                                                                                                                    self._reserve(9)
                                                                                                                    n, obj = _unpack_from('b8s', self._buffer, self._buff_i)
                                                                                                                    self._buff_i += 9
                                                                                                                else:
                                                                                                                    if b == 216:
                                                                                                                        typ = TYPE_EXT
                                                                                                                        if self._max_ext_len < 16:
                                                                                                                            raise ValueError('%s exceeds max_ext_len(%s)' % (16, self._max_ext_len))
                                                                                                                        self._reserve(17)
                                                                                                                        n, obj = _unpack_from('b16s', self._buffer, self._buff_i)
                                                                                                                        self._buff_i += 17
                                                                                                                    else:
                                                                                                                        if b == 217:
                                                                                                                            typ = TYPE_RAW
                                                                                                                            self._reserve(1)
                                                                                                                            n = self._buffer[self._buff_i]
                                                                                                                            self._buff_i += 1
                                                                                                                            if n > self._max_str_len:
                                                                                                                                raise ValueError('%s exceeds max_str_len(%s)', n, self._max_str_len)
                                                                                                                            obj = self._read(n)
                                                                                                                        else:
                                                                                                                            if b == 218:
                                                                                                                                typ = TYPE_RAW
                                                                                                                                self._reserve(2)
                                                                                                                                n, = _unpack_from('>H', self._buffer, self._buff_i)
                                                                                                                                self._buff_i += 2
                                                                                                                                if n > self._max_str_len:
                                                                                                                                    raise ValueError('%s exceeds max_str_len(%s)', n, self._max_str_len)
                                                                                                                                obj = self._read(n)
                                                                                                                            else:
                                                                                                                                if b == 219:
                                                                                                                                    typ = TYPE_RAW
                                                                                                                                    self._reserve(4)
                                                                                                                                    n, = _unpack_from('>I', self._buffer, self._buff_i)
                                                                                                                                    self._buff_i += 4
                                                                                                                                    if n > self._max_str_len:
                                                                                                                                        raise ValueError('%s exceeds max_str_len(%s)', n, self._max_str_len)
                                                                                                                                    obj = self._read(n)
                                                                                                                                else:
                                                                                                                                    if b == 220:
                                                                                                                                        typ = TYPE_ARRAY
                                                                                                                                        self._reserve(2)
                                                                                                                                        n, = _unpack_from('>H', self._buffer, self._buff_i)
                                                                                                                                        self._buff_i += 2
                                                                                                                                        if n > self._max_array_len:
                                                                                                                                            raise ValueError('%s exceeds max_array_len(%s)', n, self._max_array_len)
                                                                                                                                    elif b == 221:
                                                                                                                                        typ = TYPE_ARRAY
                                                                                                                                        self._reserve(4)
                                                                                                                                        n, = _unpack_from('>I', self._buffer, self._buff_i)
                                                                                                                                        self._buff_i += 4
                                                                                                                                        if n > self._max_array_len:
                                                                                                                                            raise ValueError('%s exceeds max_array_len(%s)', n, self._max_array_len)
                                                                                                                                    elif b == 222:
                                                                                                                                        self._reserve(2)
                                                                                                                                        n, = _unpack_from('>H', self._buffer, self._buff_i)
                                                                                                                                        self._buff_i += 2
                                                                                                                                        if n > self._max_map_len:
                                                                                                                                            raise ValueError('%s exceeds max_map_len(%s)', n, self._max_map_len)
                                                                                                                                        typ = TYPE_MAP
                                                                                                                                    else:
                                                                                                                                        if b == 223:
                                                                                                                                            self._reserve(4)
                                                                                                                                            n, = _unpack_from('>I', self._buffer, self._buff_i)
                                                                                                                                            self._buff_i += 4
                                                                                                                                            if n > self._max_map_len:
                                                                                                                                                raise ValueError('%s exceeds max_map_len(%s)', n, self._max_map_len)
                                                                                                                                            typ = TYPE_MAP
                                                                                                                                        else:
                                                                                                                                            raise FormatError('Unknown header: 0x%x' % b)
        return (
         typ, n, obj)

    def _unpack(self, execute=EX_CONSTRUCT):
        typ, n, obj = self._read_header(execute)
        if execute == EX_READ_ARRAY_HEADER:
            if typ != TYPE_ARRAY:
                raise ValueError('Expected array')
            return n
        if execute == EX_READ_MAP_HEADER:
            if typ != TYPE_MAP:
                raise ValueError('Expected map')
            return n
        if typ == TYPE_ARRAY:
            if execute == EX_SKIP:
                for i in xrange(n):
                    self._unpack(EX_SKIP)

                return
            ret = newlist_hint(n)
            for i in xrange(n):
                ret.append(self._unpack(EX_CONSTRUCT))

            if self._list_hook is not None:
                ret = self._list_hook(ret)
            if self._use_list:
                return ret
            return tuple(ret)
        if typ == TYPE_MAP:
            if execute == EX_SKIP:
                for i in xrange(n):
                    self._unpack(EX_SKIP)
                    self._unpack(EX_SKIP)

                return
            if self._object_pairs_hook is not None:
                ret = self._object_pairs_hook(((self._unpack(EX_CONSTRUCT), self._unpack(EX_CONSTRUCT)) for _ in xrange(n)))
            else:
                ret = {}
                for _ in xrange(n):
                    key = self._unpack(EX_CONSTRUCT)
                    if self._strict_map_key:
                        if type(key) not in (unicode, bytes):
                            raise ValueError('%s is not allowed for map key' % str(type(key)))
                    if not PY2:
                        if type(key) is str:
                            key = sys.intern(key)
                        ret[key] = self._unpack(EX_CONSTRUCT)

                if self._object_hook is not None:
                    ret = self._object_hook(ret)
                return ret
        if execute == EX_SKIP:
            return
        if typ == TYPE_RAW:
            if self._raw:
                obj = bytes(obj)
            else:
                obj = obj.decode('utf_8', self._unicode_errors)
            return obj
        if typ == TYPE_BIN:
            return bytes(obj)
        if typ == TYPE_EXT:
            if n == -1:
                ts = Timestamp.from_bytes(bytes(obj))
                if self._timestamp == 1:
                    return ts.to_unix()
                if self._timestamp == 2:
                    return ts.to_unix_nano()
                if self._timestamp == 3:
                    return ts.to_datetime()
                return ts
            else:
                return self._ext_hook(n, bytes(obj))
        assert typ == TYPE_IMMEDIATE
        return obj

    def __iter__(self):
        return self

    def __next__(self):
        try:
            ret = self._unpack(EX_CONSTRUCT)
            self._consume()
            return ret
        except OutOfData:
            self._consume()
            raise StopIteration
        except RecursionError:
            raise StackError

    next = __next__

    def skip(self):
        self._unpack(EX_SKIP)
        self._consume()

    def unpack(self):
        try:
            ret = self._unpack(EX_CONSTRUCT)
        except RecursionError:
            raise StackError

        self._consume()
        return ret

    def read_array_header(self):
        ret = self._unpack(EX_READ_ARRAY_HEADER)
        self._consume()
        return ret

    def read_map_header(self):
        ret = self._unpack(EX_READ_MAP_HEADER)
        self._consume()
        return ret

    def tell(self):
        return self._stream_offset


class Packer(object):
    __doc__ = "\n    MessagePack Packer\n\n    Usage:\n\n        packer = Packer()\n        astream.write(packer.pack(a))\n        astream.write(packer.pack(b))\n\n    Packer's constructor has some keyword arguments:\n\n    :param callable default:\n        Convert user type to builtin type that Packer supports.\n        See also simplejson's document.\n\n    :param bool use_single_float:\n        Use single precision float type for float. (default: False)\n\n    :param bool autoreset:\n        Reset buffer after each pack and return its content as `bytes`. (default: True).\n        If set this to false, use `bytes()` to get content and `.reset()` to clear buffer.\n\n    :param bool use_bin_type:\n        Use bin type introduced in msgpack spec 2.0 for bytes.\n        It also enables str8 type for unicode. (default: True)\n\n    :param bool strict_types:\n        If set to true, types will be checked to be exact. Derived classes\n        from serializable types will not be serialized and will be\n        treated as unsupported type and forwarded to default.\n        Additionally tuples will not be serialized as lists.\n        This is useful when trying to implement accurate serialization\n        for python types.\n\n    :param bool datetime:\n        If set to true, datetime with tzinfo is packed into Timestamp type.\n        Note that the tzinfo is stripped in the timestamp.\n        You can get UTC datetime with `timestamp=3` option of the Unpacker.\n        (Python 2 is not supported).\n\n    :param str unicode_errors:\n        The error handler for encoding unicode. (default: 'strict')\n        DO NOT USE THIS!!  This option is kept for very specific usage.\n    "

    def __init__(self, default=None, use_single_float=False, autoreset=True, use_bin_type=True, strict_types=False, datetime=False, unicode_errors=None):
        self._strict_types = strict_types
        self._use_float = use_single_float
        self._autoreset = autoreset
        self._use_bin_type = use_bin_type
        self._buffer = StringIO()
        if PY2:
            if datetime:
                raise ValueError('datetime is not supported in Python 2')
        self._datetime = bool(datetime)
        self._unicode_errors = unicode_errors or 'strict'
        if default is not None:
            if not callable(default):
                raise TypeError('default must be callable')
        self._default = default

    def _pack(self, obj, nest_limit=DEFAULT_RECURSE_LIMIT, check=isinstance, check_type_strict=_check_type_strict):
        default_used = False
        if self._strict_types:
            check = check_type_strict
            list_types = list
        else:
            list_types = (
             list, tuple)
        while 1:
            if nest_limit < 0:
                raise ValueError('recursion limit exceeded')
            else:
                if obj is None:
                    return self._buffer.write(b'\xc0')
                    if check(obj, bool):
                        if obj:
                            return self._buffer.write(b'\xc3')
                        return self._buffer.write(b'\xc2')
                    if check(obj, int_types):
                        if 0 <= obj < 128:
                            return self._buffer.write(struct.pack('B', obj))
                        else:
                            if -32 <= obj < 0:
                                return self._buffer.write(struct.pack('b', obj))
                            else:
                                if 128 <= obj <= 255:
                                    return self._buffer.write(struct.pack('BB', 204, obj))
                                else:
                                    if -128 <= obj < 0:
                                        return self._buffer.write(struct.pack('>Bb', 208, obj))
                                    else:
                                        if 255 < obj <= 65535:
                                            return self._buffer.write(struct.pack('>BH', 205, obj))
                                        else:
                                            if -32768 <= obj < -128:
                                                return self._buffer.write(struct.pack('>Bh', 209, obj))
                                            if 65535 < obj <= 4294967295:
                                                return self._buffer.write(struct.pack('>BI', 206, obj))
                                        if -2147483648 <= obj < -32768:
                                            return self._buffer.write(struct.pack('>Bi', 210, obj))
                                    if 4294967295 < obj <= 18446744073709551615:
                                        return self._buffer.write(struct.pack('>BQ', 207, obj))
                                if -9223372036854775808 <= obj < -2147483648:
                                    return self._buffer.write(struct.pack('>Bq', 211, obj))
                            if not default_used:
                                if self._default is not None:
                                    obj = self._default(obj)
                                    default_used = True
                                    continue
                        raise OverflowError('Integer value out of range')
                    if check(obj, (bytes, bytearray)):
                        n = len(obj)
                        if n >= 4294967296:
                            raise ValueError('%s is too large' % type(obj).__name__)
                        self._pack_bin_header(n)
                        return self._buffer.write(obj)
                    if check(obj, unicode):
                        obj = obj.encode('utf-8', self._unicode_errors)
                        n = len(obj)
                        if n >= 4294967296:
                            raise ValueError('String is too large')
                        self._pack_raw_header(n)
                        return self._buffer.write(obj)
                    if check(obj, memoryview):
                        n = len(obj) * obj.itemsize
                        if n >= 4294967296:
                            raise ValueError('Memoryview is too large')
                        self._pack_bin_header(n)
                        return self._buffer.write(obj)
                else:
                    if check(obj, float):
                        if self._use_float:
                            return self._buffer.write(struct.pack('>Bf', 202, obj))
                            return self._buffer.write(struct.pack('>Bd', 203, obj))
                            if check(obj, (ExtType, Timestamp)):
                                if check(obj, Timestamp):
                                    code = -1
                                    data = obj.to_bytes()
                        else:
                            code = obj.code
                            data = obj.data
                    elif not isinstance(code, int):
                        raise AssertionError
                    elif not isinstance(data, bytes):
                        raise AssertionError
                    else:
                        L = len(data)
                        if L == 1:
                            self._buffer.write(b'\xd4')
                        else:
                            if L == 2:
                                self._buffer.write(b'\xd5')
                            else:
                                if L == 4:
                                    self._buffer.write(b'\xd6')
                                else:
                                    if L == 8:
                                        self._buffer.write(b'\xd7')
                                    else:
                                        if L == 16:
                                            self._buffer.write(b'\xd8')
                                        else:
                                            if L <= 255:
                                                self._buffer.write(struct.pack('>BB', 199, L))
                                            else:
                                                if L <= 65535:
                                                    self._buffer.write(struct.pack('>BH', 200, L))
                                                else:
                                                    self._buffer.write(struct.pack('>BI', 201, L))
                    self._buffer.write(struct.pack('b', code))
                    self._buffer.write(data)
                    return
                if check(obj, list_types):
                    n = len(obj)
                    self._pack_array_header(n)
                    for i in xrange(n):
                        self._pack(obj[i], nest_limit - 1)

                    return
                if check(obj, dict):
                    return self._pack_map_pairs(len(obj), dict_iteritems(obj), nest_limit - 1)
                if self._datetime and check(obj, _DateTime):
                    obj = Timestamp.from_datetime(obj)
                    default_used = 1
                    continue
            if not default_used:
                if self._default is not None:
                    obj = self._default(obj)
                    default_used = 1
                    continue
                raise TypeError('Cannot serialize %r' % (obj,))

    def pack(self, obj):
        try:
            self._pack(obj)
        except:
            self._buffer = StringIO()
            raise

        if self._autoreset:
            ret = self._buffer.getvalue()
            self._buffer = StringIO()
            return ret

    def pack_map_pairs(self, pairs):
        self._pack_map_pairs(len(pairs), pairs)
        if self._autoreset:
            ret = self._buffer.getvalue()
            self._buffer = StringIO()
            return ret

    def pack_array_header(self, n):
        if n >= 4294967296:
            raise ValueError
        self._pack_array_header(n)
        if self._autoreset:
            ret = self._buffer.getvalue()
            self._buffer = StringIO()
            return ret

    def pack_map_header(self, n):
        if n >= 4294967296:
            raise ValueError
        self._pack_map_header(n)
        if self._autoreset:
            ret = self._buffer.getvalue()
            self._buffer = StringIO()
            return ret

    def pack_ext_type(self, typecode, data):
        if not isinstance(typecode, int):
            raise TypeError('typecode must have int type.')
        elif not 0 <= typecode <= 127:
            raise ValueError('typecode should be 0-127')
        elif not isinstance(data, bytes):
            raise TypeError('data must have bytes type')
        else:
            L = len(data)
            if L > 4294967295:
                raise ValueError('Too large data')
            elif L == 1:
                self._buffer.write(b'\xd4')
            else:
                if L == 2:
                    self._buffer.write(b'\xd5')
                else:
                    if L == 4:
                        self._buffer.write(b'\xd6')
                    else:
                        if L == 8:
                            self._buffer.write(b'\xd7')
                        else:
                            if L == 16:
                                self._buffer.write(b'\xd8')
                            else:
                                if L <= 255:
                                    self._buffer.write(b'\xc7' + struct.pack('B', L))
                                else:
                                    if L <= 65535:
                                        self._buffer.write(b'\xc8' + struct.pack('>H', L))
                                    else:
                                        self._buffer.write(b'\xc9' + struct.pack('>I', L))
        self._buffer.write(struct.pack('B', typecode))
        self._buffer.write(data)

    def _pack_array_header(self, n):
        if n <= 15:
            return self._buffer.write(struct.pack('B', 144 + n))
        if n <= 65535:
            return self._buffer.write(struct.pack('>BH', 220, n))
        if n <= 4294967295:
            return self._buffer.write(struct.pack('>BI', 221, n))
        raise ValueError('Array is too large')

    def _pack_map_header(self, n):
        if n <= 15:
            return self._buffer.write(struct.pack('B', 128 + n))
        if n <= 65535:
            return self._buffer.write(struct.pack('>BH', 222, n))
        if n <= 4294967295:
            return self._buffer.write(struct.pack('>BI', 223, n))
        raise ValueError('Dict is too large')

    def _pack_map_pairs(self, n, pairs, nest_limit=DEFAULT_RECURSE_LIMIT):
        self._pack_map_header(n)
        for k, v in pairs:
            self._pack(k, nest_limit - 1)
            self._pack(v, nest_limit - 1)

    def _pack_raw_header(self, n):
        if n <= 31:
            self._buffer.write(struct.pack('B', 160 + n))
        else:
            if self._use_bin_type and n <= 255:
                self._buffer.write(struct.pack('>BB', 217, n))
            else:
                if n <= 65535:
                    self._buffer.write(struct.pack('>BH', 218, n))
                else:
                    if n <= 4294967295:
                        self._buffer.write(struct.pack('>BI', 219, n))
                    else:
                        raise ValueError('Raw is too large')

    def _pack_bin_header(self, n):
        if not self._use_bin_type:
            return self._pack_raw_header(n)
        if n <= 255:
            return self._buffer.write(struct.pack('>BB', 196, n))
        if n <= 65535:
            return self._buffer.write(struct.pack('>BH', 197, n))
        if n <= 4294967295:
            return self._buffer.write(struct.pack('>BI', 198, n))
        raise ValueError('Bin is too large')

    def bytes(self):
        """Return internal buffer contents as bytes object"""
        return self._buffer.getvalue()

    def reset(self):
        """Reset internal buffer.

        This method is useful only when autoreset=False.
        """
        self._buffer = StringIO()

    def getbuffer(self):
        """Return view of internal buffer."""
        if USING_STRINGBUILDER or PY2:
            return memoryview(self.bytes())
        return self._buffer.getbuffer()
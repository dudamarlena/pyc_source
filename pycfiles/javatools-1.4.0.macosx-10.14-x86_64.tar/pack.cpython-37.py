# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/pack.py
# Compiled at: 2018-10-18 16:07:18
# Size of source mod 2**32: 9810 bytes
"""
Utility module for unpacking shapes of binary data from a buffer
or stream.

:author: Christopher O'Brien <obriencj@gmail.com>
:license: LGPL v.3
"""
from abc import ABCMeta, abstractmethod
from six import add_metaclass
from six.moves import range
from struct import Struct
__all__ = ('compile_struct', 'unpack', 'Unpacker', 'UnpackException', 'StreamUnpacker',
           'BufferUnpacker')
try:
    buffer
except NameError:
    buffer = memoryview

_struct_cache = dict()

def compile_struct(fmt, cache=None):
    """
    returns a struct.Struct instance compiled from fmt. If fmt has
    already been compiled, it will return the previously compiled
    Struct instance from the cache.
    """
    if cache is None:
        cache = _struct_cache
    sfmt = cache.get(fmt, None)
    if not sfmt:
        sfmt = Struct(fmt)
        cache[fmt] = sfmt
    return sfmt


@add_metaclass(ABCMeta)
class Unpacker(object):
    __doc__ = '\n    Abstract base class for `StreamUnpacker` and `BufferUnpacker`. Use\n    the `unpack` function to obtain the correct unpacker instance for\n    your data.\n    '

    def __enter__(self):
        return self

    def __exit__(self, exc_type, _exc_val, _exc_tb):
        self.close()
        return exc_type is None

    @abstractmethod
    def unpack(self, format_str):
        """
        unpacks the given format_str from the underlying data and returns
        the results. Will raise an UnpackException if there is not
        enough data to satisfy the specified format
        """
        pass

    @abstractmethod
    def unpack_struct(self, struct):
        """
        unpacks the given struct from the underlying data and returns the
        results. Will raise an UnpackException if there is not enough
        data to satisfy the format of the structure
        """
        pass

    @abstractmethod
    def read(self, count):
        """
        read count bytes from the unpacker and return it. Raises an
        UnpackException if there is not enough data in the underlying
        stream.
        """
        pass

    @abstractmethod
    def close(self):
        """
        close this unpacker and release the underlying data
        """
        pass

    def unpack_array(self, fmt):
        """
        reads a count from the unpacker, and unpacks fmt count
        times. Yields a sequence of the unpacked data tuples
        """
        count, = self.unpack_struct(_H)
        sfmt = compile_struct(fmt)
        for _i in range(count):
            yield self.unpack_struct(sfmt)

    def unpack_struct_array(self, struct):
        """
        reads a count from the unpacker, and unpacks the precompiled
        struct count times. Yields a sequence of the unpacked data
        tuples
        """
        count, = self.unpack_struct(_H)
        for _i in range(count):
            yield self.unpack_struct(struct)

    def unpack_objects(self, atype, *params, **kwds):
        """
        reads a count from the unpacker, and instanciates that many calls
        to atype, with the given params and kwds passed along. Each
        instance then has its unpack method called with this unpacker
        instance passed along. Yields a squence of the unpacked
        instances
        """
        count, = self.unpack_struct(_H)
        for _i in range(count):
            obj = atype(*params, **kwds)
            obj.unpack(self)
            yield obj


class BufferUnpacker(Unpacker):
    __doc__ = '\n    Unpacker wrapping a str or buffer.\n    '

    def __init__(self, data, offset=0):
        super(BufferUnpacker, self).__init__()
        self.data = data
        self.offset = offset

    def unpack(self, fmt):
        """
        unpacks the given fmt from the underlying buffer and returns the
        results. Will raise an UnpackException if there is not enough
        data to satisfy the fmt
        """
        sfmt = compile_struct(fmt)
        size = sfmt.size
        offset = self.offset
        if self.data:
            avail = len(self.data) - offset
        else:
            avail = 0
        if avail < size:
            raise UnpackException(fmt, size, avail)
        self.offset = offset + size
        return sfmt.unpack_from(self.data, offset)

    def unpack_struct(self, struct):
        """
        unpacks the given struct from the underlying buffer and returns
        the results. Will raise an UnpackException if there is not
        enough data to satisfy the format of the structure
        """
        size = struct.size
        offset = self.offset
        if self.data:
            avail = len(self.data) - offset
        else:
            avail = 0
        if avail < size:
            raise UnpackException(struct.format, size, avail)
        self.offset = offset + size
        return struct.unpack_from(self.data, offset)

    def read(self, count):
        """
        read count bytes from the underlying buffer and return them as a
        str. Raises an UnpackException if there is not enough data in
        the underlying buffer.
        """
        offset = self.offset
        if self.data:
            avail = len(self.data) - offset
        else:
            avail = 0
        if avail < count:
            raise UnpackException(None, count, avail)
        self.offset = offset + count
        return self.data[offset:self.offset]

    def close(self):
        """
        release the underlying buffer
        """
        self.data = None
        self.offset = 0


class StreamUnpacker(Unpacker):
    __doc__ = "\n    Wraps a stream (or creates a stream for a string or buffer) and\n    advances along it while unpacking structures from it.\n\n    This class adheres to the context management protocol, so may be\n    used in conjunction with the 'with' keyword\n    "

    def __init__(self, data):
        super(StreamUnpacker, self).__init__()
        self.data = data

    def unpack(self, fmt):
        """
        unpacks the given fmt from the underlying stream and returns the
        results. Will raise an UnpackException if there is not enough
        data to satisfy the fmt
        """
        sfmt = compile_struct(fmt)
        size = sfmt.size
        if not self.data:
            raise UnpackException(fmt, size, 0)
        buff = self.data.read(size)
        if len(buff) < size:
            raise UnpackException(fmt, size, len(buff))
        return sfmt.unpack(buff)

    def unpack_struct(self, struct):
        """
        unpacks the given struct from the underlying stream and returns
        the results. Will raise an UnpackException if there is not
        enough data to satisfy the format of the structure
        """
        size = struct.size
        if not self.data:
            raise UnpackException(struct.format, size, 0)
        buff = self.data.read(size)
        if len(buff) < size:
            raise UnpackException(struct.format, size, len(buff))
        return struct.unpack(buff)

    def read(self, count):
        """
        read count bytes from the unpacker and return it. Raises an
        UnpackException if there is not enough data in the underlying
        stream.
        """
        if not self.data:
            raise UnpackException(None, count, 0)
        buff = self.data.read(count)
        if len(buff) < count:
            raise UnpackException(None, count, len(buff))
        return buff

    def close(self):
        """
        close this unpacker, and the underlying stream if it supports such
        """
        data = self.data
        self.data = None
        if hasattr(data, 'close'):
            data.close()


def unpack(data):
    """
    returns either a BufferUnpacker or StreamUnpacker instance,
    depending upon the type of data. The unpacker supports the managed
    context interface, so may be used eg: `with unpack(my_data) as
    unpacker:`
    """
    if isinstance(data, (bytes, buffer)):
        return BufferUnpacker(data)
    if hasattr(data, 'read'):
        return StreamUnpacker(data)
    raise TypeError('unpack requires bytes, buffer, or instance supporting the read method')


class UnpackException(Exception):
    __doc__ = '\n    raised when there is not enough data to unpack the expected\n    structures\n    '
    template = 'format %r requires %i bytes, only %i present'

    def __init__(self, fmt, wanted, present):
        msg = self.template % (fmt, wanted, present)
        super(UnpackException, self).__init__(msg)
        self.format = fmt
        self.bytes_wanted = wanted
        self.bytes_present = present


_H = compile_struct('>H')
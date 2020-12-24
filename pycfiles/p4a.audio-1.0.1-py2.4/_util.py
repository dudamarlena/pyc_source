# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/ogg/thirdparty/mutagen/_util.py
# Compiled at: 2007-11-27 08:43:15
"""Utility classes for Mutagen.

You should not rely on the interfaces here being stable. They are
intended for internal use in Mutagen only.
"""
import struct, mmap

class DictMixin(object):
    """Implement the dict API using keys() and __*item__ methods.

    Similar to UserDict.DictMixin, this takes a class that defines
    __getitem__, __setitem__, __delitem__, and keys(), and turns it
    into a full dict-like object.

    UserDict.DictMixin is not suitable for this purpose because it's
    an old-style class.

    This class is not optimized for very large dictionaries; many
    functions have linear memory requirements. I recommend you
    override some of these functions if speed is required.
    """
    __module__ = __name__

    def __iter__(self):
        return iter(self.keys())

    def has_key(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    __contains__ = has_key
    iterkeys = lambda self: iter(self.keys())

    def values(self):
        return map(self.__getitem__, self.keys())

    itervalues = lambda self: iter(self.values())

    def items(self):
        return zip(self.keys(), self.values())

    iteritems = lambda s: iter(s.items())

    def clear(self):
        map(self.__delitem__, self.keys())

    def pop(self, key, *args):
        if len(args) > 1:
            raise TypeError('pop takes at most two arguments')
        try:
            value = self[key]
        except KeyError:
            if args:
                return args[0]
            else:
                raise

        del self[key]
        return value

    def popitem(self):
        try:
            key = self.keys()[0]
            return (key, self.pop(key))
        except IndexError:
            raise KeyError('dictionary is empty')

    def update(self, other=None, **kwargs):
        if other is None:
            self.update(kwargs)
            other = {}
        try:
            map(self.__setitem__, other.keys(), other.values())
        except AttributeError:
            for (key, value) in other:
                self[key] = value

        return

    def setdefault(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            self[key] = default
            return default

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __repr__(self):
        return repr(dict(self.items()))

    def __cmp__(self, other):
        if other is None:
            return 1
        else:
            return cmp(dict(self.items()), other)
        return

    def __len__(self):
        return len(self.keys())


class cdata(object):
    """C character buffer to Python numeric type conversions."""
    __module__ = __name__
    from struct import error
    short_le = staticmethod(lambda data: struct.unpack('<h', data)[0])
    ushort_le = staticmethod(lambda data: struct.unpack('<H', data)[0])
    short_be = staticmethod(lambda data: struct.unpack('>h', data)[0])
    ushort_be = staticmethod(lambda data: struct.unpack('>H', data)[0])
    int_le = staticmethod(lambda data: struct.unpack('<i', data)[0])
    uint_le = staticmethod(lambda data: struct.unpack('<I', data)[0])
    int_be = staticmethod(lambda data: struct.unpack('>i', data)[0])
    uint_be = staticmethod(lambda data: struct.unpack('>I', data)[0])
    longlong_le = staticmethod(lambda data: struct.unpack('<q', data)[0])
    ulonglong_le = staticmethod(lambda data: struct.unpack('<Q', data)[0])
    to_short_le = staticmethod(lambda data: struct.pack('<h', data))
    to_ushort_le = staticmethod(lambda data: struct.pack('<H', data))
    to_short_be = staticmethod(lambda data: struct.pack('>h', data))
    to_ushort_be = staticmethod(lambda data: struct.pack('>H', data))
    to_int_le = staticmethod(lambda data: struct.pack('<i', data))
    to_uint_le = staticmethod(lambda data: struct.pack('<I', data))
    to_int_be = staticmethod(lambda data: struct.pack('>i', data))
    to_uint_be = staticmethod(lambda data: struct.pack('>I', data))
    to_longlong_le = staticmethod(lambda data: struct.pack('<q', data))
    to_ulonglong_le = staticmethod(lambda data: struct.pack('<Q', data))
    to_longlong_be = staticmethod(lambda data: struct.pack('>q', data))
    to_ulonglong_be = staticmethod(lambda data: struct.pack('>Q', data))
    bitswap = ('').join([ chr(sum([ (val >> i & 1) << 7 - i for i in range(8) ])) for val in range(256) ])
    del i
    del val
    test_bit = staticmethod(lambda value, n: bool(value >> n & 1))


def insert_bytes(fobj, size, offset):
    """Insert size bytes of empty space starting at offset.

    fobj must be an open file object, open rb+ or
    equivalent. Mutagen tries to use mmap to resize the file, but
    falls back to a significantly slower method if mmap fails.
    """
    assert 0 < size
    assert 0 <= offset
    fobj.seek(0, 2)
    filesize = fobj.tell()
    movesize = filesize - offset
    fobj.write('\x00' * size)
    fobj.flush()
    try:
        map = mmap.mmap(fobj.fileno(), filesize + size)
        try:
            map.move(offset + size, offset, movesize)
        finally:
            map.close()
    except (ValueError, EnvironmentError):
        fobj.truncate(filesize)
        fobj.seek(offset)
        backbuf = fobj.read(size)
        offset += len(backbuf)
        if len(backbuf) < size:
            fobj.seek(offset)
            fobj.write('\x00' * (size - len(backbuf)))
        while len(backbuf) == size:
            frontbuf = fobj.read(size)
            fobj.seek(offset)
            fobj.write(backbuf)
            offset += len(backbuf)
            fobj.seek(offset)
            backbuf = frontbuf

        fobj.write(backbuf)


def delete_bytes(fobj, size, offset):
    """Delete size bytes of empty space starting at offset.

    fobj must be an open file object, open rb+ or
    equivalent. Mutagen tries to use mmap to resize the file, but
    falls back to a significantly slower method if mmap fails.
    """
    assert 0 < size
    assert 0 <= offset
    fobj.seek(0, 2)
    filesize = fobj.tell()
    movesize = filesize - offset - size
    assert 0 <= movesize
    if movesize > 0:
        fobj.flush()
        try:
            map = mmap.mmap(fobj.fileno(), filesize)
            try:
                map.move(offset, offset + size, movesize)
            finally:
                map.close()
        except (ValueError, EnvironmentError):
            fobj.seek(offset + size)
            buf = fobj.read(size)
            while len(buf):
                fobj.seek(offset)
                fobj.write(buf)
                offset += len(buf)
                fobj.seek(offset + size)
                buf = fobj.read(size)

    fobj.truncate(filesize - size)
    fobj.flush()


def utf8(data):
    """Convert a basestring to a valid UTF-8 str."""
    if isinstance(data, str):
        return data.decode('utf-8', 'replace').encode('utf-8')
    elif isinstance(data, unicode):
        return data.encode('utf-8')
    else:
        raise TypeError('only unicode/str types can be converted to UTF-8')
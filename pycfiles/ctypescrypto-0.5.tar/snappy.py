# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/snappy.py
# Compiled at: 2011-11-22 11:11:50
from ctypes import byref, cdll, create_string_buffer, c_char_p, c_int
__all__ = [
 'compress', 'uncompress', 'decompress']
try:
    lib_snappy = cdll.LoadLibrary('libsnappy.so.1')
    __snappy_max_compressed_length = lib_snappy.snappy_max_compressed_length
    __snappy_compress = lib_snappy.snappy_compress
    __snappy_uncompress = lib_snappy.snappy_uncompress
    __snappy_uncompressed_length = lib_snappy.snappy_uncompressed_length
except OSError:
    raise ImportError, 'Snappy DLL not found.'

class SnappyException(Exception):
    pass


def compress(s):
    """Compress the string using snappy."""
    cbuf = create_string_buffer(__snappy_max_compressed_length(len(s)))
    clen = c_int(__snappy_max_compressed_length(len(s)))
    cresult = __snappy_compress(c_char_p(s), len(s), cbuf, byref(clen))
    if cresult != 0:
        raise SnappyException, 'Error in snappy_compress: %d' % cresult
    return cbuf.raw[:clen.value]


def uncompress(s):
    """Uncompress a snappy compressed string."""
    ulen = c_int(0)
    cresult = __snappy_uncompressed_length(s, len(s), byref(ulen))
    if cresult != 0:
        raise SnappyException, 'Error in snappy_uncompressed_length: %d' % cresult
    ubuf = create_string_buffer(ulen.value)
    __snappy_uncompress(s, len(s), ubuf, byref(ulen))
    if cresult != 0:
        raise SnappyException, 'Error in snappy_uncompress: %d' % cresult
    return ubuf.raw


decompress = uncompress
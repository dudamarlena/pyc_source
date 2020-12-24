# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/common/deflate.py
# Compiled at: 2009-09-07 17:44:28
from hachoir_core.field import CompressedField
try:
    from zlib import decompressobj, MAX_WBITS

    class DeflateStream:
        __module__ = __name__

        def __init__(self, stream, wbits=None):
            if wbits:
                self.gzip = decompressobj(-MAX_WBITS)
            else:
                self.gzip = decompressobj()

        def __call__(self, size, data=None):
            if data is None:
                data = self.gzip.unconsumed_tail
            return self.gzip.decompress(data, size)


    class DeflateStreamWbits(DeflateStream):
        __module__ = __name__

        def __init__(self, stream):
            DeflateStream.__init__(self, stream, True)


    def Deflate(field, wbits=True):
        if wbits:
            CompressedField(field, DeflateStreamWbits)
        else:
            CompressedField(field, DeflateStream)
        return field


    has_deflate = True
except ImportError:

    def Deflate(field, wbits=True):
        return field


    has_deflate = False
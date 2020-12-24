# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\reconstruct\lib\utils.py
# Compiled at: 2010-05-01 15:45:14
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from struct import Struct as Packer
except ImportError:
    from struct import pack, unpack, calcsize

    class Packer(object):
        __slots__ = [
         'format', 'size']

        def __init__(self, format):
            self.format = format
            self.size = calcsize(format)

        def pack(self, *args):
            return pack(self.format, *args)

        def unpack(self, data):
            return unpack(self.format, data)
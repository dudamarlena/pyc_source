# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Support/whoosh/support/bitstream.py
# Compiled at: 2015-06-30 06:52:38
__doc__ = '\n\nFrom a post by Patrick Maupin on the Python mailing list:\nhttp://mail.python.org/pipermail/python-list/2003-November/237481.html\n'
from array import array
from whoosh.system import _ULONG_SIZE
_bitsperlong = _ULONG_SIZE * 8

class BitStreamReader(object):

    def __init__(self, source):
        self._totalbits = len(source) * _bitsperlong
        self._position = 0
        source += -len(source) % _ULONG_SIZE * chr(0)
        bits = array('L')
        bits.fromstring(source)
        self._bitstream = bits

    def seek(self, offset):
        self._position = offset

    def tell(self):
        return self._position

    def read(self, numbits):
        position = self._position
        if position < 0 or position + numbits > self._totalbits:
            raise IndexError, 'Invalid bitarray._position/numbits'
        longaddress, bitoffset = divmod(position, _bitsperlong)
        finalmask = (1 << numbits) - 1
        numbits += bitoffset
        outval, outshift = (0, 0)
        while numbits > 0:
            outval += self._bitstream[longaddress] << outshift
            longaddress += 1
            outshift += _bitsperlong
            numbits -= _bitsperlong

        self._position = longaddress * _bitsperlong + numbits
        return outval >> bitoffset & finalmask
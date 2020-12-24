# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ssb/shs/util.py
# Compiled at: 2018-09-02 03:33:39
# Size of source mod 2**32: 3722 bytes
import struct
from io import BytesIO
NONCE_SIZE = 24
MAX_NONCE = 8 * NONCE_SIZE

class AsyncBuffer(BytesIO):
    __doc__ = 'Just a BytesIO with an async read method.'

    async def read(self, n=None):
        v = super(AsyncBuffer, self).read(n)
        return v

    readexactly = read

    def append(self, data):
        """Append data to the buffer without changing the current position."""
        pos = self.tell()
        self.write(data)
        self.seek(pos)


async def async_comprehend(generator):
    """Emulate ``[elem async for elem in generator]``."""
    results = []
    async for msg in generator:
        results.append(msg)

    return results


def inc_nonce(nonce):
    num = bytes_to_long(nonce) + 1
    if num > 2 ** MAX_NONCE:
        num = 0
    bnum = long_to_bytes(num)
    bnum = b'\x00' * (NONCE_SIZE - len(bnum)) + bnum
    return bnum


def split_chunks(seq, n):
    """Split sequence in equal-sized chunks.
    The last chunk is not padded."""
    while seq:
        yield seq[:n]
        seq = seq[n:]


def b(s):
    return s.encode('latin-1')


def long_to_bytes(n, blocksize=0):
    """long_to_bytes(n:long, blocksize:int) : string
    Convert a long integer to a byte string.
    If optional blocksize is given and greater than zero, pad the front of the
    byte string with binary zeros so that the length is a multiple of
    blocksize.
    """
    s = b('')
    pack = struct.pack
    while n > 0:
        s = pack('>I', n & 4294967295) + s
        n = n >> 32

    for i in range(len(s)):
        if s[i] != b('\x00')[0]:
            break
    else:
        s = b('\x00')
        i = 0

    s = s[i:]
    if blocksize > 0:
        if len(s) % blocksize:
            s = (blocksize - len(s) % blocksize) * b('\x00') + s
    return s


def bytes_to_long(s):
    """bytes_to_long(string) : long
    Convert a byte string to a long integer.
    This is (essentially) the inverse of long_to_bytes().
    """
    acc = 0
    unpack = struct.unpack
    length = len(s)
    if length % 4:
        extra = 4 - length % 4
        s = b('\x00') * extra + s
        length = length + extra
    for i in range(0, length, 4):
        acc = (acc << 32) + unpack('>I', s[i:i + 4])[0]

    return acc
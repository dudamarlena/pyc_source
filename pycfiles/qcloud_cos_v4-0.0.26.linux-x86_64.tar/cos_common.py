# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.14/lib/python2.7/site-packages/qcloud_cos/cos_common.py
# Compiled at: 2018-03-19 03:53:29
from __future__ import print_function
import struct, io
try:
    range = xrange
except NameError:
    pass

def _left_rotate(n, b):
    """Left rotate a 32-bit integer n by b bits."""
    return (n << b | n >> 32 - b) & 4294967295


def _process_chunk(chunk, h0, h1, h2, h3, h4):
    """Process a chunk of data and return the new digest variables."""
    assert len(chunk) == 64
    w = [
     0] * 80
    for i in range(16):
        w[i] = struct.unpack('>I', chunk[i * 4:i * 4 + 4])[0]

    for i in range(16, 80):
        w[i] = _left_rotate(w[(i - 3)] ^ w[(i - 8)] ^ w[(i - 14)] ^ w[(i - 16)], 1)

    a = h0
    b = h1
    c = h2
    d = h3
    e = h4
    for i in range(80):
        if 0 <= i <= 19:
            f = d ^ b & (c ^ d)
            k = 1518500249
        elif 20 <= i <= 39:
            f = b ^ c ^ d
            k = 1859775393
        elif 40 <= i <= 59:
            f = b & c | b & d | c & d
            k = 2400959708
        elif 60 <= i <= 79:
            f = b ^ c ^ d
            k = 3395469782
        a, b, c, d, e = (_left_rotate(a, 5) + f + e + k + w[i] & 4294967295,
         a, _left_rotate(b, 30), c, d)

    h0 = h0 + a & 4294967295
    h1 = h1 + b & 4294967295
    h2 = h2 + c & 4294967295
    h3 = h3 + d & 4294967295
    h4 = h4 + e & 4294967295
    return (
     h0, h1, h2, h3, h4)


class Sha1Hash(object):
    """A class that mimics that hashlib api and implements the SHA-1 algorithm."""
    name = 'python-sha1'
    digest_size = 20
    block_size = 64

    def __init__(self):
        self._h = (1732584193, 4023233417, 2562383102, 271733878, 3285377520)
        self._unprocessed = ''
        self._message_byte_length = 0

    def update(self, arg):
        """Update the current digest.
        This may be called repeatedly, even after calling digest or hexdigest.

        Arguments:
            arg: bytes, bytearray, or BytesIO object to read from.
        """
        if isinstance(arg, (bytes, bytearray)):
            arg = io.BytesIO(arg)
        chunk = self._unprocessed + arg.read(64 - len(self._unprocessed))
        while len(chunk) == 64:
            self._h = _process_chunk(chunk, *self._h)
            self._message_byte_length += 64
            chunk = arg.read(64)

        self._unprocessed = chunk
        return self

    def digest(self):
        """Produce the final hash value (big-endian) as a bytes object"""
        return ('').join(struct.pack('>I', h) for h in self._produce_digest())

    def hexdigest(self):
        """Produce the final hash value (big-endian) as a hex string"""
        return '%08x%08x%08x%08x%08x' % self._produce_digest()

    def inner_digest(self):
        tmp = struct.unpack('>5I', struct.pack('<5I', *self._h))
        return '%08x%08x%08x%08x%08x' % tmp

    def _produce_digest(self):
        """Return finalized digest variables for the data processed so far."""
        message = self._unprocessed
        message_byte_length = self._message_byte_length + len(message)
        message += b'\x80'
        message += '\x00' * ((56 - (message_byte_length + 1) % 64) % 64)
        message_bit_length = message_byte_length * 8
        message += struct.pack('>Q', message_bit_length)
        h = _process_chunk(message[:64], *self._h)
        if len(message) == 64:
            return h
        return _process_chunk(message[64:], *h)


def sha1(data):
    """SHA-1 Hashing Function
    A custom SHA-1 hashing function implemented entirely in Python.
    Arguments:
        data: A bytes or BytesIO object containing the input message to hash.
    Returns:
        A hex SHA-1 digest of the input message.
    """
    return Sha1Hash().update(data).hexdigest()


class Sha1Util(object):

    @staticmethod
    def get_sha1_by_slice(file_name, slice_size):
        u""" Get SHA array based on Qcloud Slice Upload Interface

        :param file_name: local file path
        :param slice_size: slice size in bit
        :return: sha array like [{“offset”:0, “datalen”:1024,”datasha”:”aaa”}, {}, {}]
        """
        from os import path
        with open(file_name, 'rb') as (f):
            result = []
            file_size = path.getsize(file_name)
            sha1_obj = Sha1Hash()
            for current_offset in range(0, file_size, slice_size):
                data_length = min(slice_size, file_size - current_offset)
                sha1_obj.update(f.read(data_length))
                sha1_val = sha1_obj.inner_digest()
                result.append({'offset': current_offset, 'datalen': data_length, 'datasha': sha1_val})

            result[(-1)]['datasha'] = sha1_obj.hexdigest()
            return result


if __name__ == '__main__':
    import argparse, sys, os
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', help='input file or message to hash')
    args = parser.parse_args()
    data = None
    if args.input is None:
        try:
            data = sys.stdin.detach()
        except AttributeError:
            if sys.platform == 'win32':
                import msvcrt
                msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
            data = sys.stdin

    elif os.path.isfile(args.input):
        data = open(args.input, 'rb')
    else:
        data = args.input
    print('sha1-digest:', sha1(data))
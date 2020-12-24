# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ISEN\AppData\Local\Temp\pip-install-57ghrzot\pyserial\serial\tools\hexlify_codec.py
# Compiled at: 2019-09-23 21:15:07
# Size of source mod 2**32: 3637 bytes
"""Python 'hex' Codec - 2-digit hex with spaces content transfer encoding.

Encode and decode may be a bit missleading at first sight...

The textual representation is a hex dump: e.g. "40 41"
The "encoded" data of this is the binary form, e.g. b"@A"

Therefore decoding is binary to text and thus converting binary data to hex dump.

"""
import codecs, serial
try:
    unicode
except (NameError, AttributeError):
    unicode = str

HEXDIGITS = '0123456789ABCDEF'

def hex_encode(data, errors='strict'):
    """'40 41 42' -> b'@ab'"""
    return (
     serial.to_bytes([int(h, 16) for h in data.split()]), len(data))


def hex_decode(data, errors='strict'):
    """b'@ab' -> '40 41 42'"""
    return (
     unicode(''.join(('{:02X} '.format(ord(b)) for b in serial.iterbytes(data)))), len(data))


class Codec(codecs.Codec):

    def encode(self, data, errors='strict'):
        """'40 41 42' -> b'@ab'"""
        return serial.to_bytes([int(h, 16) for h in data.split()])

    def decode(self, data, errors='strict'):
        """b'@ab' -> '40 41 42'"""
        return unicode(''.join(('{:02X} '.format(ord(b)) for b in serial.iterbytes(data))))


class IncrementalEncoder(codecs.IncrementalEncoder):
    __doc__ = 'Incremental hex encoder'

    def __init__(self, errors='strict'):
        self.errors = errors
        self.state = 0

    def reset(self):
        self.state = 0

    def getstate(self):
        return self.state

    def setstate(self, state):
        self.state = state

    def encode(self, data, final=False):
        """        Incremental encode, keep track of digits and emit a byte when a pair
        of hex digits is found. The space is optional unless the error
        handling is defined to be 'strict'.
        """
        state = self.state
        encoded = []
        for c in data.upper():
            if c in HEXDIGITS:
                z = HEXDIGITS.index(c)
                if state:
                    encoded.append(z + (state & 240))
                    state = 0
                else:
                    state = 256 + (z << 4)
            else:
                if c == ' ':
                    if state:
                        if self.errors == 'strict':
                            raise UnicodeError('odd number of hex digits')
                    state = 0

        self.state = state
        return serial.to_bytes(encoded)


class IncrementalDecoder(codecs.IncrementalDecoder):
    __doc__ = 'Incremental decoder'

    def decode(self, data, final=False):
        return unicode(''.join(('{:02X} '.format(ord(b)) for b in serial.iterbytes(data))))


class StreamWriter(Codec, codecs.StreamWriter):
    __doc__ = 'Combination of hexlify codec and StreamWriter'


class StreamReader(Codec, codecs.StreamReader):
    __doc__ = 'Combination of hexlify codec and StreamReader'


def getregentry():
    """encodings module API"""
    return codecs.CodecInfo(name='hexlify',
      encode=hex_encode,
      decode=hex_decode,
      incrementalencoder=IncrementalEncoder,
      incrementaldecoder=IncrementalDecoder,
      streamwriter=StreamWriter,
      streamreader=StreamReader)
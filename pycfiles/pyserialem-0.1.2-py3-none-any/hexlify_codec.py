# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/tools/hexlify_codec.py
# Compiled at: 2015-08-29 23:08:08
__doc__ = "Python 'hex' Codec - 2-digit hex with spaces content transfer encoding.\n"
import codecs, serial
HEXDIGITS = '0123456789ABCDEF'

def hex_encode(input, errors='strict'):
    return (
     serial.to_bytes([ int(h, 16) for h in input.split() ]), len(input))


def hex_decode(input, errors='strict'):
    return (
     ('').join(('{:02X} ').format(b) for b in input), len(input))


class Codec(codecs.Codec):

    def encode(self, input, errors='strict'):
        return serial.to_bytes([ int(h, 16) for h in input.split() ])

    def decode(self, input, errors='strict'):
        return ('').join(('{:02X} ').format(b) for b in input)


class IncrementalEncoder(codecs.IncrementalEncoder):

    def __init__(self, errors='strict'):
        self.errors = errors
        self.state = 0

    def reset(self):
        self.state = 0

    def getstate(self):
        return self.state

    def setstate(self, state):
        self.state = state

    def encode(self, input, final=False):
        state = self.state
        encoded = []
        for c in input.upper():
            if c in HEXDIGITS:
                z = HEXDIGITS.index(c)
                if state:
                    encoded.append(z + (state & 240))
                    state = 0
                else:
                    state = 256 + (z << 4)
            elif c == ' ':
                if state and self.errors == 'strict':
                    raise UnicodeError('odd number of hex digits')
                state = 0
            elif self.errors == 'strict':
                raise UnicodeError('non-hex digit found: %r' % c)

        self.state = state
        return serial.to_bytes(encoded)


class IncrementalDecoder(codecs.IncrementalDecoder):

    def decode(self, input, final=False):
        return ('').join(('{:02X} ').format(b) for b in input)


class StreamWriter(Codec, codecs.StreamWriter):
    pass


class StreamReader(Codec, codecs.StreamReader):
    pass


def getregentry():
    return codecs.CodecInfo(name='hexlify', encode=hex_encode, decode=hex_decode, incrementalencoder=IncrementalEncoder, incrementaldecoder=IncrementalDecoder, streamwriter=StreamWriter, streamreader=StreamReader, _is_text_encoding=True)
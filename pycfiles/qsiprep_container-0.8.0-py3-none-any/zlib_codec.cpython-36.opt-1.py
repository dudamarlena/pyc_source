# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/circleci/.pyenv/versions/3.6.5/lib/python3.6/zlib_codec.py
# Compiled at: 2019-03-22 00:31:37
# Size of source mod 2**32: 2204 bytes
"""Python 'zlib_codec' Codec - zlib compression encoding.

This codec de/encodes from bytes to bytes.

Written by Marc-Andre Lemburg (mal@lemburg.com).
"""
import codecs, zlib

def zlib_encode(input, errors='strict'):
    return (
     zlib.compress(input), len(input))


def zlib_decode(input, errors='strict'):
    return (
     zlib.decompress(input), len(input))


class Codec(codecs.Codec):

    def encode(self, input, errors='strict'):
        return zlib_encode(input, errors)

    def decode(self, input, errors='strict'):
        return zlib_decode(input, errors)


class IncrementalEncoder(codecs.IncrementalEncoder):

    def __init__(self, errors='strict'):
        self.errors = errors
        self.compressobj = zlib.compressobj()

    def encode(self, input, final=False):
        if final:
            c = self.compressobj.compress(input)
            return c + self.compressobj.flush()
        else:
            return self.compressobj.compress(input)

    def reset(self):
        self.compressobj = zlib.compressobj()


class IncrementalDecoder(codecs.IncrementalDecoder):

    def __init__(self, errors='strict'):
        self.errors = errors
        self.decompressobj = zlib.decompressobj()

    def decode(self, input, final=False):
        if final:
            c = self.decompressobj.decompress(input)
            return c + self.decompressobj.flush()
        else:
            return self.decompressobj.decompress(input)

    def reset(self):
        self.decompressobj = zlib.decompressobj()


class StreamWriter(Codec, codecs.StreamWriter):
    charbuffertype = bytes


class StreamReader(Codec, codecs.StreamReader):
    charbuffertype = bytes


def getregentry():
    return codecs.CodecInfo(name='zlib',
      encode=zlib_encode,
      decode=zlib_decode,
      incrementalencoder=IncrementalEncoder,
      incrementaldecoder=IncrementalDecoder,
      streamreader=StreamReader,
      streamwriter=StreamWriter,
      _is_text_encoding=False)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/circleci/.pyenv/versions/3.6.5/lib/python3.6/hex_codec.py
# Compiled at: 2019-03-22 00:31:37
# Size of source mod 2**32: 1508 bytes
import codecs, binascii

def hex_encode(input, errors='strict'):
    return (
     binascii.b2a_hex(input), len(input))


def hex_decode(input, errors='strict'):
    return (
     binascii.a2b_hex(input), len(input))


class Codec(codecs.Codec):

    def encode(self, input, errors='strict'):
        return hex_encode(input, errors)

    def decode(self, input, errors='strict'):
        return hex_decode(input, errors)


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final=False):
        return binascii.b2a_hex(input)


class IncrementalDecoder(codecs.IncrementalDecoder):

    def decode(self, input, final=False):
        return binascii.a2b_hex(input)


class StreamWriter(Codec, codecs.StreamWriter):
    charbuffertype = bytes


class StreamReader(Codec, codecs.StreamReader):
    charbuffertype = bytes


def getregentry():
    return codecs.CodecInfo(name='hex',
      encode=hex_encode,
      decode=hex_decode,
      incrementalencoder=IncrementalEncoder,
      incrementaldecoder=IncrementalDecoder,
      streamwriter=StreamWriter,
      streamreader=StreamReader,
      _is_text_encoding=False)
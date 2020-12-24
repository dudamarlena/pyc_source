# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/circleci/.pyenv/versions/3.6.5/lib/python3.6/base64_codec.py
# Compiled at: 2019-03-22 00:31:37
# Size of source mod 2**32: 1533 bytes
"""Python 'base64_codec' Codec - base64 content transfer encoding.

This codec de/encodes from bytes to bytes.

Written by Marc-Andre Lemburg (mal@lemburg.com).
"""
import codecs, base64

def base64_encode(input, errors='strict'):
    return (
     base64.encodebytes(input), len(input))


def base64_decode(input, errors='strict'):
    return (
     base64.decodebytes(input), len(input))


class Codec(codecs.Codec):

    def encode(self, input, errors='strict'):
        return base64_encode(input, errors)

    def decode(self, input, errors='strict'):
        return base64_decode(input, errors)


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final=False):
        return base64.encodebytes(input)


class IncrementalDecoder(codecs.IncrementalDecoder):

    def decode(self, input, final=False):
        return base64.decodebytes(input)


class StreamWriter(Codec, codecs.StreamWriter):
    charbuffertype = bytes


class StreamReader(Codec, codecs.StreamReader):
    charbuffertype = bytes


def getregentry():
    return codecs.CodecInfo(name='base64',
      encode=base64_encode,
      decode=base64_decode,
      incrementalencoder=IncrementalEncoder,
      incrementaldecoder=IncrementalDecoder,
      streamwriter=StreamWriter,
      streamreader=StreamReader,
      _is_text_encoding=False)
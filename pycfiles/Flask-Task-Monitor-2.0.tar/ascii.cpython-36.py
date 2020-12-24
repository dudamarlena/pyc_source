# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/encodings/ascii.py
# Compiled at: 2018-03-28 06:24:30
# Size of source mod 2**32: 1248 bytes
""" Python 'ascii' Codec

Written by Marc-Andre Lemburg (mal@lemburg.com).

(c) Copyright CNRI, All Rights Reserved. NO WARRANTY.

"""
import codecs

class Codec(codecs.Codec):
    encode = codecs.ascii_encode
    decode = codecs.ascii_decode


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final=False):
        return codecs.ascii_encode(input, self.errors)[0]


class IncrementalDecoder(codecs.IncrementalDecoder):

    def decode(self, input, final=False):
        return codecs.ascii_decode(input, self.errors)[0]


class StreamWriter(Codec, codecs.StreamWriter):
    pass


class StreamReader(Codec, codecs.StreamReader):
    pass


class StreamConverter(StreamWriter, StreamReader):
    encode = codecs.ascii_decode
    decode = codecs.ascii_encode


def getregentry():
    return codecs.CodecInfo(name='ascii',
      encode=(Codec.encode),
      decode=(Codec.decode),
      incrementalencoder=IncrementalEncoder,
      incrementaldecoder=IncrementalDecoder,
      streamwriter=StreamWriter,
      streamreader=StreamReader)
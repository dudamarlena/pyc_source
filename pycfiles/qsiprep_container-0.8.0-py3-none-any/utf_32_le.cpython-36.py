# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/circleci/.pyenv/versions/3.6.5/lib/python3.6/utf_32_le.py
# Compiled at: 2019-03-22 00:31:37
# Size of source mod 2**32: 930 bytes
"""
Python 'utf-32-le' Codec
"""
import codecs
encode = codecs.utf_32_le_encode

def decode(input, errors='strict'):
    return codecs.utf_32_le_decode(input, errors, True)


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final=False):
        return codecs.utf_32_le_encode(input, self.errors)[0]


class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    _buffer_decode = codecs.utf_32_le_decode


class StreamWriter(codecs.StreamWriter):
    encode = codecs.utf_32_le_encode


class StreamReader(codecs.StreamReader):
    decode = codecs.utf_32_le_decode


def getregentry():
    return codecs.CodecInfo(name='utf-32-le',
      encode=encode,
      decode=decode,
      incrementalencoder=IncrementalEncoder,
      incrementaldecoder=IncrementalDecoder,
      streamreader=StreamReader,
      streamwriter=StreamWriter)
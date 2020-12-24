# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/circleci/.pyenv/versions/3.6.5/lib/python3.6/oem.py
# Compiled at: 2019-03-22 00:31:37
# Size of source mod 2**32: 1019 bytes
from codecs import oem_encode, oem_decode
import codecs
encode = oem_encode

def decode(input, errors='strict'):
    return oem_decode(input, errors, True)


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final=False):
        return oem_encode(input, self.errors)[0]


class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    _buffer_decode = oem_decode


class StreamWriter(codecs.StreamWriter):
    encode = oem_encode


class StreamReader(codecs.StreamReader):
    decode = oem_decode


def getregentry():
    return codecs.CodecInfo(name='oem',
      encode=encode,
      decode=decode,
      incrementalencoder=IncrementalEncoder,
      incrementaldecoder=IncrementalDecoder,
      streamreader=StreamReader,
      streamwriter=StreamWriter)
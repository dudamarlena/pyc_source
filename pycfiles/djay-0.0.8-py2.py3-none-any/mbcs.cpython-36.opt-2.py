# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ant/.pyenv/versions/3.6.5/lib/python3.6/mbcs.py
# Compiled at: 2019-07-30 17:44:47
# Size of source mod 2**32: 1211 bytes
from codecs import mbcs_encode, mbcs_decode
import codecs
encode = mbcs_encode

def decode(input, errors='strict'):
    return mbcs_decode(input, errors, True)


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final=False):
        return mbcs_encode(input, self.errors)[0]


class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    _buffer_decode = mbcs_decode


class StreamWriter(codecs.StreamWriter):
    encode = mbcs_encode


class StreamReader(codecs.StreamReader):
    decode = mbcs_decode


def getregentry():
    return codecs.CodecInfo(name='mbcs',
      encode=encode,
      decode=decode,
      incrementalencoder=IncrementalEncoder,
      incrementaldecoder=IncrementalDecoder,
      streamreader=StreamReader,
      streamwriter=StreamWriter)
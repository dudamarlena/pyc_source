# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/circleci/.pyenv/versions/3.6.5/lib/python3.6/cp65001.py
# Compiled at: 2019-03-22 00:31:37
# Size of source mod 2**32: 1106 bytes
"""
Code page 65001: Windows UTF-8 (CP_UTF8).
"""
import codecs, functools
if not hasattr(codecs, 'code_page_encode'):
    raise LookupError('cp65001 encoding is only available on Windows')
encode = functools.partial(codecs.code_page_encode, 65001)
_decode = functools.partial(codecs.code_page_decode, 65001)

def decode(input, errors='strict'):
    return codecs.code_page_decode(65001, input, errors, True)


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final=False):
        return encode(input, self.errors)[0]


class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    _buffer_decode = _decode


class StreamWriter(codecs.StreamWriter):
    encode = encode


class StreamReader(codecs.StreamReader):
    decode = _decode


def getregentry():
    return codecs.CodecInfo(name='cp65001',
      encode=encode,
      decode=decode,
      incrementalencoder=IncrementalEncoder,
      incrementaldecoder=IncrementalDecoder,
      streamreader=StreamReader,
      streamwriter=StreamWriter)
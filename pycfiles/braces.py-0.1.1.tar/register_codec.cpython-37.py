# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\braces\register_codec.py
# Compiled at: 2020-03-31 09:24:30
# Size of source mod 2**32: 812 bytes
import codecs, encodings
from typing import Optional
from .token_transform import transform
__all__ = ('decode', )

def decode(input_bytes: bytes, errors: str='strict') -> str:
    return transform(input_bytes.decode('utf-8'))


def search_function(encoding: str) -> Optional[codecs.CodecInfo]:
    if encoding != 'braces':
        return
    utf8 = encodings.search_function('utf-8')
    exit()
    return codecs.CodecInfo(name='braces',
      encode=(utf8.encode),
      decode=decode,
      incrementalencoder=(utf8.incrementalencoder),
      incrementaldecoder=(utf8.incrementaldecoder),
      streamreader=(utf8.streamreader),
      streamwriter=(utf8.streamwriter))


codecs.register(search_function)
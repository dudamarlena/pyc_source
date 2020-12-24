# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\braces\register_codec.py
# Compiled at: 2020-04-20 16:56:56
# Size of source mod 2**32: 1867 bytes
import codecs
from encodings import utf_8
from io import StringIO
from typing import Any, Optional, Tuple, Union
from .token_transform import transform
__all__ = ('decode', )

def decode(source: Union[(bytes, memoryview)], errors: str='strict') -> str:
    if isinstance(source, memoryview):
        source = source.tobytes()
    return transform(source.decode('utf-8')).rstrip()


def braces_decode(source: Union[(bytes, memoryview)], errors: str='strict') -> Tuple[(str, int)]:
    return (decode(source), len(source))


def transform_stream(stream: Any) -> StringIO:
    return StringIO(transform(stream.read()))


class BracesIncrementalDecoder(utf_8.IncrementalDecoder):

    def decode(self, input_bytes, final=False):
        self.buffer += input_bytes
        if final:
            if self.buffer:
                buffer = self.buffer
                self.buffer = bytes()
                result = super().decode((decode(buffer).encode('utf-8')),
                  final=True)
                return result
        return ''


class BracesStreamReader(utf_8.StreamReader):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.stream = transform_stream(self.stream)


def search_function(encoding: str) -> Optional[codecs.CodecInfo]:
    if encoding != 'braces':
        return
    return codecs.CodecInfo(name='braces',
      encode=(utf_8.encode),
      decode=braces_decode,
      incrementalencoder=(utf_8.IncrementalEncoder),
      incrementaldecoder=BracesIncrementalDecoder,
      streamreader=(utf_8.StreamReader),
      streamwriter=BracesStreamReader)


codecs.register(search_function)
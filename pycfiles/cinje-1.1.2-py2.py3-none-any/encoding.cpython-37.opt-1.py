# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cinje/encoding.py
# Compiled at: 2018-11-21 11:13:57
# Size of source mod 2**32: 1440 bytes
from __future__ import unicode_literals
import codecs
from encodings import utf_8 as utf8
from .util import StringIO, bytes, str, Context

def transform(input):
    translator = Context(input)
    return '\n'.join((str(i) for i in translator.stream))


def cinje_decode(input, errors='strict', final=True):
    if not final:
        return ('', 0)
    output = transform(bytes(input).decode('utf8', errors))
    return (output, len(input))


class CinjeIncrementalDecoder(utf8.IncrementalDecoder):

    def _buffer_decode(self, input, errors='strict', final=False):
        if not final or len(input) == 0:
            return ('', 0)
        output = transform(bytes(input).decode('utf8', errors))
        return (
         output, len(input))


class CinjeStreamReader(utf8.StreamReader):

    def __init__(self, *args, **kw):
        (codecs.StreamReader.__init__)(self, *args, **kw)
        self.stream = StringIO(transform(self.stream))


def cinje_search_function(name):
    if name != 'cinje':
        return
    return codecs.CodecInfo(name='cinje',
      encode=(utf8.encode),
      decode=cinje_decode,
      incrementalencoder=None,
      incrementaldecoder=CinjeIncrementalDecoder,
      streamreader=CinjeStreamReader,
      streamwriter=(utf8.StreamWriter))


codecs.register(cinje_search_function)
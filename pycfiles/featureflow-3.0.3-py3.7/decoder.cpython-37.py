# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/featureflow/decoder.py
# Compiled at: 2019-03-01 22:03:23
# Size of source mod 2**32: 2555 bytes
import json
from .util import chunked
from .extractor import Node
import bz2
from dill import loads
from io import StringIO

class Decoder(object):
    __doc__ = '\n    The simplest possible decoder takes a file-like object and returns it\n    '

    def __init__(self):
        super(Decoder, self).__init__()

    def __call__(self, flo):
        return flo

    def __iter__(self, flo):
        for chunk in chunked(flo):
            yield chunk


class TextDecoder(Decoder):

    def __init__(self):
        super().__init__()

    def __call__(self, flo):
        return StringIO(flo.read().decode())

    def __iter__(self):
        for chunk in super().__iter__(self.flo):
            yield chunk.decode()


class GreedyDecoder(Decoder):
    __doc__ = '\n    A decoder that reads the entire file contents into memory\n    '

    def __init__(self):
        super(GreedyDecoder, self).__init__()

    def __call__(self, flo):
        return flo.read()

    def __iter__(self, flo):
        yield self(flo)


class GreedyTextDecoder(TextDecoder):

    def __init__(self):
        super().__init__()

    def __call__(self, flo):
        return flo.read().decode()

    def __iter__(self, flo):
        yield self(flo)


class JSONDecoder(GreedyTextDecoder):
    __doc__ = '\n    A decoder that interprets the data as JSON\n    '

    def __init__(self):
        super(JSONDecoder, self).__init__()

    def __call__(self, flo):
        s = super(JSONDecoder, self).__call__(flo)
        return json.loads(s)

    def __iter__(self, flo):
        yield self(flo)


class PickleDecoder(GreedyDecoder):

    def __init__(self):
        super(PickleDecoder, self).__init__()

    def __call__(self, flo):
        return loads(flo.read())

    def __iter__(self, flo):
        yield self(flo)


class BZ2Decoder(Decoder):
    __doc__ = '\n    A decoder that decompresses data using the bz2 compression algorithm\n    '

    def __init__(self):
        super(BZ2Decoder, self).__init__()

    def __call__(self, flo):
        return self.__iter__(flo)

    def __iter__(self, flo):
        decompressor = bz2.BZ2Decompressor()
        for chunk in chunked(flo):
            yield decompressor.decompress(chunk)


class DecoderNode(Node):

    def __init__(self, needs=None, decodifier=None, version=None):
        super(DecoderNode, self).__init__(needs=needs)
        self._version = version
        self.decoder = decodifier

    @property
    def version(self):
        return self._version

    def _process(self, data):
        for x in self.decoder.__iter__(data):
            yield x
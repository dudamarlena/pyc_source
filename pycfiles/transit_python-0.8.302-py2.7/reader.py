# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/transit/reader.py
# Compiled at: 2017-12-12 16:52:26
import json, msgpack
from collections import OrderedDict
from transit import sosjson
from transit.decoder import Decoder

class Reader(object):
    """The top-level object for reading in Transit data and converting it to
    Python objects.  During initialization, you must specify the protocol used
    for unmarshalling the data- json or msgpack.
    """

    def __init__(self, protocol='json'):
        if protocol in ('json', 'json_verbose'):
            self.reader = JsonUnmarshaler()
        elif protocol == 'msgpack':
            self.reader = MsgPackUnmarshaler()
            self.unpacker = self.reader.unpacker
        else:
            raise ValueError("'" + protocol + "' is not a supported. " + 'Protocol must be:' + "'json', 'json_verbose', or 'msgpack'.")

    def read(self, stream):
        """Given a readable file descriptor object (something `load`able by
        msgpack or json), read the data, and return the Python representation
        of the contents. One-shot reader.
        """
        return self.reader.load(stream)

    def register(self, key_or_tag, f_val):
        """Register a custom transit tag and decoder/parser function for use
        during reads.
        """
        self.reader.decoder.register(key_or_tag, f_val)

    def readeach(self, stream, **kwargs):
        """Temporary hook for API while streaming reads are in experimental
        phase. Read each object from stream as available with generator.
        JSON blocks indefinitely waiting on JSON entities to arrive. MsgPack
        requires unpacker property to be fed stream using unpacker.feed()
        method.
        """
        for o in self.reader.loadeach(stream):
            yield o


class JsonUnmarshaler(object):
    """The top-level Unmarshaler used by the Reader for JSON payloads.  While
    you may use this directly, it is strongly discouraged.
    """

    def __init__(self):
        self.decoder = Decoder()

    def load(self, stream):
        return self.decoder.decode(json.load(stream, object_pairs_hook=OrderedDict))

    def loadeach(self, stream):
        for o in sosjson.items(stream, object_pairs_hook=OrderedDict):
            yield self.decoder.decode(o)


class MsgPackUnmarshaler(object):
    """The top-level Unmarshaler used by the Reader for MsgPack payloads.
    While you may use this directly, it is strongly discouraged.
    """

    def __init__(self):
        self.decoder = Decoder()
        self.unpacker = msgpack.Unpacker(object_pairs_hook=OrderedDict)

    def load(self, stream):
        return self.decoder.decode(msgpack.load(stream, object_pairs_hook=OrderedDict))

    def loadeach(self, stream):
        for o in self.unpacker:
            yield self.decoder.decode(o)
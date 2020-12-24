# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aiogcd/connector/path.py
# Compiled at: 2019-09-11 07:21:09
# Size of source mod 2**32: 1618 bytes
__doc__ = 'path.py\n\nCreated on: May 19, 2017\n    Author: Jeroen van der Heijden <jeroen@transceptor.technology>\n'
from .pathelement import PathElement
from .pathelement import path_element_from_decoder
from .buffer import BufferDecodeError

def path_from_decoder(decoder):
    pairs = []
    while decoder:
        tt = decoder.get_var_int32()
        if tt == 11:
            pairs.append(path_element_from_decoder(decoder))
            continue
        if tt == 0:
            raise BufferDecodeError('corrupted')

    return Path(pairs=pairs)


class Path:

    def __init__(self, pairs):
        self._path = tuple(((pe if isinstance(pe, PathElement) else PathElement(*pe)) for pe in pairs))

    def encode(self, buffer):
        buffer.add_var_int32(114)
        buffer.add_var_int32(self.byte_size)
        for path_element in self._path:
            buffer.add_var_int32(11)
            path_element.encode(buffer)
            buffer.add_var_int32(12)

    def __getitem__(self, item):
        return self._path.__getitem__(item)

    def __repr__(self):
        return str(self.get_as_tuple())

    def get_dict(self):
        return {'path': [pe.get_dict() for pe in self._path]}

    @property
    def byte_size(self):
        n = 2 * len(self._path)
        for path_element in self._path:
            n += path_element.byte_size

        return n

    def get_as_tuple(self):
        """Returns a tuple of pairs (tuples) representing the key path of an
        entity. Useful for composing entities with a specific ancestor."""
        return tuple(((pe.kind, pe.id) for pe in self._path))
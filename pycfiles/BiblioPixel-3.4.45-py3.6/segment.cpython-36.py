# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/layout/geometry/segment.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1539 bytes
from . import strip

class Segment(strip.Strip):
    __doc__ = 'Represents an offset, length segment within a strip.'

    def __init__(self, strip, length, offset=0):
        if offset < 0 or length < 0:
            raise ValueError('Segment indices are non-negative.')
        if offset + length > len(strip):
            raise ValueError('Segment too long.')
        self.strip = strip
        self.offset = offset
        self.length = length

    def __getitem__(self, index):
        return self.strip[self._fix_index(index)]

    def __setitem__(self, index, value):
        self.strip[self._fix_index(index)] = value

    def __len__(self):
        return self.length

    def next(self, length):
        """Return a new segment starting right after self in the same buffer."""
        return Segment(self.strip, length, self.offset + self.length)

    def _fix_index(self, index):
        if isinstance(index, slice):
            raise ValueError('Slicing segments not implemented.')
        else:
            if index < 0:
                index += self.length
            if index >= 0:
                if index < self.length:
                    return self.offset + index
        raise IndexError('Index out of range')


def make_segments(strip, length):
    """Return a list of Segments that evenly split the strip."""
    if len(strip) % length:
        raise ValueError('The length of strip must be a multiple of length')
    s = []
    try:
        while True:
            s.append(s[(-1)].next(length) if s else Segment(strip, length))

    except ValueError:
        return s
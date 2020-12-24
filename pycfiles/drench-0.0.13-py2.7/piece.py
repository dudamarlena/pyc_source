# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/drench/piece.py
# Compiled at: 2013-12-10 13:58:10
from bitarray import bitarray

class Piece(object):

    def __init__(self, index=None, num_blocks=None, request_size=None):
        assert index is not None
        assert num_blocks is not None
        assert request_size is not None
        self.index = index
        self.bitfield = bitarray('1' * num_blocks)
        self.num_blocks = num_blocks
        self.request_size = request_size
        self.data = {}
        return

    def save(self, index=None, bytes=None):
        self.data[index] = bytes
        self.bitfield[index] = False

    def get_bytes(self):
        result = ''
        for i in sorted(self.data.keys()):
            result += self.data.pop(i)

        assert self.data == {}
        assert type(result) == str
        return result

    @property
    def complete(self):
        if any(self.bitfield):
            return False
        else:
            return True

    @property
    def last_block(self):
        return (self.num_blocks - 1) * self.request_size


def tests():
    length = 5
    my_piece = Piece(1, length)
    for i in xrange(length):
        my_piece.save(index=i, bytes=str(i))

    assert my_piece.complete
    print my_piece.bitfield
    print my_piece.get_bytes()


if __name__ == '__main__':
    tests()
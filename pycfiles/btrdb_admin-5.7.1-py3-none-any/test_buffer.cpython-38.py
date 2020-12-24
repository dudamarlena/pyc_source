# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/tests/btrdb/utils/test_buffer.py
# Compiled at: 2019-03-06 16:01:18
# Size of source mod 2**32: 4332 bytes
__doc__ = '\nTesting for the btrdb.collection module\n'
import pytest
from btrdb.utils.buffer import PointBuffer
from btrdb.point import RawPoint

class TestPointBuffer(object):

    def test_earliest(self):
        """
        Assert earliest returns correct key
        """
        buffer = PointBuffer(3)
        buffer[2000][0] = 'horse'
        buffer[1000][0] = 'zebra'
        buffer[1000][1] = 'leopard'
        buffer[1000][2] = 'giraffe'
        buffer[3000][0] = 'pig'
        assert buffer.earliest() == 1000

    def test_earliest_if_empty(self):
        """
        Assert earliest return None
        """
        buffer = PointBuffer(3)
        assert buffer.earliest() == None

    def test_next_key_ready(self):
        """
        Assert next_key_ready returns correct key
        """
        buffer = PointBuffer(3)
        buffer.add_point(0, RawPoint(time=1000, value='zebra'))
        buffer.add_point(1, RawPoint(time=1000, value='leopard'))
        buffer.add_point(2, RawPoint(time=1000, value='giraffe'))
        buffer.add_point(0, RawPoint(time=2000, value='horse'))
        buffer.add_point(0, RawPoint(time=3000, value='pig'))
        assert buffer.next_key_ready() == 1000
        buffer = PointBuffer(2)
        buffer.add_point(0, RawPoint(time=1000, value='horse'))
        buffer.add_point(0, RawPoint(time=2000, value='zebra'))
        buffer.add_point(0, RawPoint(time=3000, value='pig'))
        buffer.add_point(1, RawPoint(time=2000, value='leopard'))
        assert buffer.next_key_ready() == 1000

    def test_next_key_ready_if_none_are(self):
        """
        Assert next_key_ready returns None if nothing is ready
        """
        buffer = PointBuffer(3)
        assert buffer.next_key_ready() == None
        buffer.add_point(0, RawPoint(time=1000, value='leopard'))
        buffer.add_point(2, RawPoint(time=1000, value='giraffe'))
        buffer.add_point(0, RawPoint(time=2000, value='horse'))
        buffer.add_point(0, RawPoint(time=3000, value='pig'))
        assert buffer.next_key_ready() == None

    def test_deactivate(self):
        """
        Assert deactivate modifies active list correctly
        """
        buffer = PointBuffer(3)
        buffer.deactivate(1)
        assert buffer.active == [True, False, True]

    def test_is_ready(self):
        """
        Assert is_ready returns correct value
        """
        buffer = PointBuffer(2)
        buffer.add_point(0, RawPoint(time=1000, value='zebra'))
        buffer.add_point(1, RawPoint(time=1000, value='giraffe'))
        buffer.add_point(0, RawPoint(time=2000, value='horse'))
        assert buffer.is_ready(1000) == True
        assert buffer.is_ready(2000) == False
        buffer.deactivate(1)
        assert buffer.is_ready(2000) == True

    def test_next_key_ready_with_inactive(self):
        """
        Assert next_key_ready returns correct key with inactive stream
        """
        buffer = PointBuffer(3)
        buffer.deactivate(1)
        buffer.add_point(0, RawPoint(time=1000, value='leopard'))
        buffer.add_point(2, RawPoint(time=1000, value='leopard'))
        buffer.add_point(0, RawPoint(time=2000, value='leopard'))
        assert buffer.next_key_ready() == 1000
        buffer = PointBuffer(3)
        buffer.add_point(1, RawPoint(time=500, value='leopard'))
        buffer.deactivate(1)
        buffer.add_point(0, RawPoint(time=1000, value='leopard'))
        buffer.add_point(2, RawPoint(time=1000, value='leopard'))
        assert buffer.next_key_ready() == 500
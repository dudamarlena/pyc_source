# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/js/dev/prl/dart/pybind11/python/tests/unit/simulation/test_world.py
# Compiled at: 2018-10-11 07:27:53
# Size of source mod 2**32: 257 bytes
import unittest
from dartpy.simulation import World

class TestWorld(unittest.TestCase):

    def test_empty_world(self):
        world = World.create()


if __name__ == '__main__':
    unittest.main()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ngen/tests/test_utils.py
# Compiled at: 2017-10-08 17:55:08
from __future__ import unicode_literals, absolute_import, print_function
import unittest
from ngen.utils import cached_property, chunk

class Thing(object):
    multiplier = 0

    def __init__(self, multiplier):
        self.multiplier = multiplier

    @cached_property
    def stuff(self):
        return self.multiplier * 3


class UtilsTests(unittest.TestCase):

    def setUp(self):
        self.instance = Thing(4)

    def test_cached_property_on_class(self):
        self.assertIsInstance(Thing.stuff, cached_property)

    def test_cached_property(self):
        self.assertTrue(b'stuff' not in self.instance.__dict__)
        self.assertTrue(b'stuff' in dir(self.instance))
        getattr(self.instance, b'stuff')
        self.assertTrue(b'stuff' in self.instance.__dict__)
        self.instance.__dict__[b'stuff'] = b'aha!'
        self.assertEqual(self.instance.stuff, b'aha!')
        del self.instance.__dict__[b'stuff']
        self.assertEqual(self.instance.stuff, 12)

    def test_chunk(self):
        array = range(10)
        chunky = chunk(array, 2)
        self.assertEqual(len(chunky), 5)
        self.assertEqual(len(chunky[0]), 2)
        self.assertEqual(len(chunky[(-1)]), 2)
        chunky = chunk(array, 3)
        self.assertEqual(len(chunky), 4)
        self.assertEqual(len(chunky[0]), 3)
        self.assertEqual(len(chunky[(-1)]), 1)
        chunky = chunk(array, 3, strict=True)
        self.assertEqual(len(chunky), 3)
        self.assertEqual(len(chunky[0]), 3)
        self.assertEqual(len(chunky[(-1)]), 3)
        chunky = chunk(tuple(array), 3, strict=True)
        self.assertEqual(len(chunky), 3)
        self.assertEqual(len(chunky[0]), 3)
        self.assertEqual(len(chunky[(-1)]), 3)


if __name__ == b'__main__':
    unittest.main()
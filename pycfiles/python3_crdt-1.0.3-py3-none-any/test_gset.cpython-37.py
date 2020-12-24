# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gg/PycharmProjects/gg-python3-crdt/build/lib/tests/test_gset.py
# Compiled at: 2019-04-22 02:28:32
# Size of source mod 2**32: 2145 bytes
import unittest, uuid, set_sys_path
from gset import GSet

class TestLWW(unittest.TestCase):

    def setUp(self):
        self.gset1 = GSet(uuid.uuid4())
        self.gset2 = GSet(uuid.uuid4())
        self.gset1.add('a')
        self.gset1.add('b')
        self.gset2.add('b')
        self.gset2.add('c')
        self.gset2.add('d')

    def test_elements_add_correctly_gset(self):
        self.assertEqual(self.gset1.payload, ['a', 'b'])
        self.assertEqual(self.gset2.payload, ['b', 'c', 'd'])

    def test_querying_gset_without_merging(self):
        self.assertTrue(self.gset1.query('a'))
        self.assertTrue(self.gset1.query('b'))
        self.assertFalse(self.gset1.query('c'))
        self.assertFalse(self.gset1.query('d'))
        self.assertFalse(self.gset2.query('a'))
        self.assertTrue(self.gset2.query('b'))
        self.assertTrue(self.gset2.query('c'))
        self.assertTrue(self.gset2.query('d'))

    def test_merging_gset(self):
        self.gset1.merge(self.gset2)
        self.assertEqual(self.gset1.payload, ['a', 'b', 'c', 'd'])
        self.gset2.merge(self.gset1)
        self.assertEqual(self.gset2.payload, ['a', 'b', 'c', 'd'])
        self.assertEqual(self.gset1.payload, self.gset2.payload)

    def test_querying_gset_with_merging(self):
        self.gset2.merge(self.gset1)
        self.assertTrue(self.gset2.query('a'))
        self.assertTrue(self.gset2.query('b'))
        self.assertTrue(self.gset2.query('c'))
        self.assertTrue(self.gset2.query('d'))
        self.gset1.merge(self.gset2)
        self.assertTrue(self.gset1.query('a'))
        self.assertTrue(self.gset1.query('b'))
        self.assertTrue(self.gset1.query('c'))
        self.assertTrue(self.gset1.query('d'))


if __name__ == '__main__':
    unittest.main()
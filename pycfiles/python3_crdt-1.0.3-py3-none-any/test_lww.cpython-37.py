# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gg/PycharmProjects/gg-python3-crdt/build/lib/tests/test_lww.py
# Compiled at: 2019-04-22 02:28:32
# Size of source mod 2**32: 5481 bytes
import unittest, uuid, set_sys_path
from lww import LWWElementSet as LWWSet

class TestLWW(unittest.TestCase):

    def setUp(self):
        self.lww1 = LWWSet(uuid.uuid4())
        self.lww2 = LWWSet(uuid.uuid4())
        self.lww1.add('a')
        self.lww1.add('b')
        self.lww2.add('b')
        self.lww2.add('c')
        self.lww2.add('d')

    def test_elements_add_correctly_lww_set(self):
        self.assertEqual([_['elem'] for _ in self.lww1.A], ['a', 'b'])
        self.assertEqual([_['elem'] for _ in self.lww1.R], [])
        self.assertEqual([_['elem'] for _ in self.lww2.A], ['b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.lww2.R], [])

    def test_querying_lww_set_without_removal_and_merging(self):
        self.assertTrue(self.lww1.query('a'))
        self.assertTrue(self.lww1.query('b'))
        self.assertFalse(self.lww1.query('c'))
        self.assertFalse(self.lww1.query('d'))
        self.assertFalse(self.lww2.query('a'))
        self.assertTrue(self.lww2.query('b'))
        self.assertTrue(self.lww2.query('c'))
        self.assertTrue(self.lww2.query('d'))

    def test_merging_lww_set_without_removal(self):
        self.lww1.merge(self.lww2)
        self.assertEqual([_['elem'] for _ in self.lww1.A], ['a', 'b', 'b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.lww1.R], [])
        self.lww2.merge(self.lww1)
        self.assertEqual([_['elem'] for _ in self.lww2.A], ['a', 'b', 'b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.lww2.R], [])
        self.assertEqual([_['elem'] for _ in self.lww1.A], [_['elem'] for _ in self.lww2.A])
        self.assertEqual([_['elem'] for _ in self.lww1.R], [_['elem'] for _ in self.lww2.R])

    def test_querying_lww_set_with_merging_without_removal(self):
        self.lww2.merge(self.lww1)
        self.assertTrue(self.lww2.query('a'))
        self.assertTrue(self.lww2.query('b'))
        self.assertTrue(self.lww2.query('c'))
        self.assertTrue(self.lww2.query('d'))
        self.lww1.merge(self.lww2)
        self.assertTrue(self.lww1.query('a'))
        self.assertTrue(self.lww1.query('b'))
        self.assertTrue(self.lww1.query('c'))
        self.assertTrue(self.lww1.query('d'))

    def test_elements_remove_correctly_lww_set(self):
        self.lww1.remove('b')
        self.assertEqual([_['elem'] for _ in self.lww1.A], ['a', 'b'])
        self.assertEqual([_['elem'] for _ in self.lww1.R], ['b'])
        self.lww2.remove('b')
        self.lww2.remove('c')
        self.assertEqual([_['elem'] for _ in self.lww2.A], ['b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.lww2.R], ['b', 'c'])

    def test_querying_lww_set_without_merging_with_removal(self):
        self.lww1.remove('b')
        self.assertTrue(self.lww1.query('a'))
        self.assertFalse(self.lww1.query('b'))
        self.assertFalse(self.lww1.query('c'))
        self.assertFalse(self.lww1.query('d'))
        self.lww2.remove('b')
        self.lww2.remove('c')
        self.assertFalse(self.lww2.query('a'))
        self.assertFalse(self.lww2.query('b'))
        self.assertFalse(self.lww2.query('c'))
        self.assertTrue(self.lww2.query('d'))

    def test_merging_lww_set_with_removal(self):
        self.lww1.remove('b')
        self.lww2.remove('b')
        self.lww2.remove('c')
        self.lww1.merge(self.lww2)
        self.assertEqual([_['elem'] for _ in self.lww1.A], ['a', 'b', 'b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.lww1.R], ['b', 'b', 'c'])
        self.lww2.merge(self.lww1)
        self.assertEqual([_['elem'] for _ in self.lww2.A], ['a', 'b', 'b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.lww2.R], ['b', 'b', 'c'])
        self.assertEqual([_['elem'] for _ in self.lww1.A], [_['elem'] for _ in self.lww2.A])
        self.assertEqual([_['elem'] for _ in self.lww1.R], [_['elem'] for _ in self.lww2.R])

    def test_querying_lww_set_with_merging_with_removal(self):
        self.lww1.remove('b')
        self.lww2.remove('b')
        self.lww2.remove('c')
        self.lww1.merge(self.lww2)
        self.lww2.merge(self.lww1)
        self.assertTrue(self.lww1.query('a'))
        self.assertFalse(self.lww1.query('b'))
        self.assertFalse(self.lww1.query('c'))
        self.assertTrue(self.lww1.query('d'))
        self.assertTrue(self.lww2.query('a'))
        self.assertFalse(self.lww2.query('b'))
        self.assertFalse(self.lww2.query('c'))
        self.assertTrue(self.lww2.query('d'))


if __name__ == '__main__':
    unittest.main()
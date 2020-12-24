# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gg/PycharmProjects/gg-python3-crdt/build/lib/tests/test_orset.py
# Compiled at: 2019-04-22 02:28:32
# Size of source mod 2**32: 6277 bytes
import unittest, uuid, set_sys_path
from orset import ORSet

class TestORSet(unittest.TestCase):

    def setUp(self):
        self.orset1 = ORSet(uuid.uuid4())
        self.orset2 = ORSet(uuid.uuid4())
        self.orset1.add('a', uuid.uuid4())
        self.orset1.add('b', uuid.uuid4())
        self.orset2.add('b', uuid.uuid4())
        self.orset2.add('c', uuid.uuid4())
        self.orset2.add('d', uuid.uuid4())

    def test_elements_add_correctly_orset(self):
        self.assertEqual([_['elem'] for _ in self.orset1.A], ['a', 'b'])
        self.assertEqual([_['elem'] for _ in self.orset1.R], [])
        self.assertEqual([_['elem'] for _ in self.orset2.A], ['b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.orset2.R], [])

    def test_querying_orset_without_removal_and_merging(self):
        self.assertTrue(self.orset1.query('a'))
        self.assertTrue(self.orset1.query('b'))
        self.assertFalse(self.orset1.query('c'))
        self.assertFalse(self.orset1.query('d'))
        self.assertFalse(self.orset2.query('a'))
        self.assertTrue(self.orset2.query('b'))
        self.assertTrue(self.orset2.query('c'))
        self.assertTrue(self.orset2.query('d'))

    def test_merging_orset_without_removal(self):
        self.orset1.merge(self.orset2)
        self.assertEqual([_['elem'] for _ in self.orset1.A], ['a', 'b', 'c', 'd'])
        for _ in self.orset1.A:
            if _['elem'] == 'b':
                self.assertEqual(len(_['tags']), 2)
                break

        self.assertEqual([_['elem'] for _ in self.orset1.R], [])
        self.orset2.merge(self.orset1)
        self.assertEqual([_['elem'] for _ in self.orset2.A], ['a', 'b', 'c', 'd'])
        for _ in self.orset2.A:
            if _['elem'] == 'b':
                self.assertEqual(len(_['tags']), 2)
                break

        self.assertEqual([_['elem'] for _ in self.orset2.R], [])
        self.assertEqual([_['elem'] for _ in self.orset1.A], [_['elem'] for _ in self.orset2.A])
        self.assertEqual([_['elem'] for _ in self.orset1.R], [_['elem'] for _ in self.orset2.R])

    def test_querying_orset_with_merging_without_removal(self):
        self.orset2.merge(self.orset1)
        self.assertTrue(self.orset2.query('a'))
        self.assertTrue(self.orset2.query('b'))
        self.assertTrue(self.orset2.query('c'))
        self.assertTrue(self.orset2.query('d'))
        self.orset1.merge(self.orset2)
        self.assertTrue(self.orset1.query('a'))
        self.assertTrue(self.orset1.query('b'))
        self.assertTrue(self.orset1.query('c'))
        self.assertTrue(self.orset1.query('d'))

    def test_elements_remove_correctly_orset(self):
        self.orset1.remove('b')
        self.assertEqual([_['elem'] for _ in self.orset1.A], ['a', 'b'])
        self.assertEqual([_['elem'] for _ in self.orset1.R], ['b'])
        self.orset2.remove('b')
        self.orset2.remove('c')
        self.assertEqual([_['elem'] for _ in self.orset2.A], ['b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.orset2.R], ['b', 'c'])

    def test_querying_orset_without_merging_with_removal(self):
        self.orset1.remove('b')
        self.assertTrue(self.orset1.query('a'))
        self.assertFalse(self.orset1.query('b'))
        self.assertFalse(self.orset1.query('c'))
        self.assertFalse(self.orset1.query('d'))
        self.orset2.remove('b')
        self.orset2.remove('c')
        self.assertFalse(self.orset2.query('a'))
        self.assertFalse(self.orset2.query('b'))
        self.assertFalse(self.orset2.query('c'))
        self.assertTrue(self.orset2.query('d'))

    def test_merging_orset_with_removal(self):
        self.orset1.remove('b')
        self.orset2.remove('b')
        self.orset2.remove('c')
        self.orset1.merge(self.orset2)
        self.assertEqual([_['elem'] for _ in self.orset1.A], ['a', 'b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.orset1.R], ['b', 'c'])
        for _ in self.orset1.R:
            if _['elem'] == 'b':
                self.assertEqual(len(_['tags']), 2)
                break

        self.orset2.merge(self.orset1)
        self.assertEqual([_['elem'] for _ in self.orset2.A], ['a', 'b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.orset2.R], ['b', 'c'])
        for _ in self.orset2.R:
            if _['elem'] == 'b':
                self.assertEqual(len(_['tags']), 2)
                break

        self.assertEqual([_['elem'] for _ in self.orset1.A], [_['elem'] for _ in self.orset2.A])
        self.assertEqual([_['elem'] for _ in self.orset1.R], [_['elem'] for _ in self.orset2.R])

    def test_querying_orset_with_merging_with_removal(self):
        self.orset1.remove('b')
        self.orset2.remove('b')
        self.orset2.remove('c')
        self.orset1.merge(self.orset2)
        self.orset2.merge(self.orset1)
        self.assertTrue(self.orset1.query('a'))
        self.assertFalse(self.orset1.query('b'))
        self.assertFalse(self.orset1.query('c'))
        self.assertTrue(self.orset1.query('d'))
        self.assertTrue(self.orset2.query('a'))
        self.assertFalse(self.orset2.query('b'))
        self.assertFalse(self.orset2.query('c'))
        self.assertTrue(self.orset2.query('d'))


if __name__ == '__main__':
    unittest.main()
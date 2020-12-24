# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gg/PycharmProjects/gg-python3-crdt/build/lib/tests/test_twopset.py
# Compiled at: 2019-04-22 02:28:32
# Size of source mod 2**32: 5599 bytes
import unittest, uuid, set_sys_path
from twopset import TwoPSet

class TestLWW(unittest.TestCase):

    def setUp(self):
        self.twopset1 = TwoPSet(uuid.uuid4())
        self.twopset2 = TwoPSet(uuid.uuid4())
        self.twopset1.add('a')
        self.twopset1.add('b')
        self.twopset2.add('b')
        self.twopset2.add('c')
        self.twopset2.add('d')

    def test_elements_add_correctly_twopset(self):
        self.assertEqual(self.twopset1.A.payload, ['a', 'b'])
        self.assertEqual(self.twopset1.R.payload, [])
        self.assertEqual(self.twopset2.A.payload, ['b', 'c', 'd'])
        self.assertEqual(self.twopset2.R.payload, [])

    def test_querying_twopset_without_removal_and_merging(self):
        self.assertTrue(self.twopset1.query('a'))
        self.assertTrue(self.twopset1.query('b'))
        self.assertFalse(self.twopset1.query('c'))
        self.assertFalse(self.twopset1.query('d'))
        self.assertFalse(self.twopset2.query('a'))
        self.assertTrue(self.twopset2.query('b'))
        self.assertTrue(self.twopset2.query('c'))
        self.assertTrue(self.twopset2.query('d'))

    def test_merging_twopset_without_removal(self):
        self.twopset1.merge(self.twopset2)
        self.assertEqual(self.twopset1.A.payload, ['a', 'b', 'c', 'd'])
        self.assertEqual(self.twopset1.R.payload, [])
        self.twopset2.merge(self.twopset1)
        self.assertEqual(self.twopset2.A.payload, ['a', 'b', 'c', 'd'])
        self.assertEqual(self.twopset2.R.payload, [])
        self.assertEqual(self.twopset1.A.payload, self.twopset2.A.payload)
        self.assertEqual(self.twopset1.R.payload, self.twopset2.R.payload)

    def test_querying_twopset_with_merging_without_removal(self):
        self.twopset2.merge(self.twopset1)
        self.assertTrue(self.twopset2.query('a'))
        self.assertTrue(self.twopset2.query('b'))
        self.assertTrue(self.twopset2.query('c'))
        self.assertTrue(self.twopset2.query('d'))
        self.twopset1.merge(self.twopset2)
        self.assertTrue(self.twopset1.query('a'))
        self.assertTrue(self.twopset1.query('b'))
        self.assertTrue(self.twopset1.query('c'))
        self.assertTrue(self.twopset1.query('d'))

    def test_elements_remove_correctly_twopset(self):
        self.twopset1.remove('b')
        self.assertEqual(self.twopset1.A.payload, ['a', 'b'])
        self.assertEqual(self.twopset1.R.payload, ['b'])
        self.twopset2.remove('b')
        self.twopset2.remove('c')
        self.assertEqual(self.twopset2.A.payload, ['b', 'c', 'd'])
        self.assertEqual(self.twopset2.R.payload, ['b', 'c'])

    def test_querying_twopset_without_merging_with_removal(self):
        self.twopset1.remove('b')
        self.assertTrue(self.twopset1.query('a'))
        self.assertFalse(self.twopset1.query('b'))
        self.assertFalse(self.twopset1.query('c'))
        self.assertFalse(self.twopset1.query('d'))
        self.twopset2.remove('b')
        self.twopset2.remove('c')
        self.assertFalse(self.twopset2.query('a'))
        self.assertFalse(self.twopset2.query('b'))
        self.assertFalse(self.twopset2.query('c'))
        self.assertTrue(self.twopset2.query('d'))

    def test_merging_twopset_with_removal(self):
        self.twopset1.remove('b')
        self.twopset2.remove('b')
        self.twopset2.remove('c')
        self.twopset1.merge(self.twopset2)
        self.assertEqual(self.twopset1.A.payload, ['a', 'b', 'c', 'd'])
        self.assertEqual(self.twopset1.R.payload, ['b', 'c'])
        self.twopset2.merge(self.twopset1)
        self.assertEqual(self.twopset2.A.payload, ['a', 'b', 'c', 'd'])
        self.assertEqual(self.twopset2.R.payload, ['b', 'c'])
        self.assertEqual(self.twopset1.A.payload, self.twopset2.A.payload)
        self.assertEqual(self.twopset1.R.payload, self.twopset2.R.payload)

    def test_querying_twopset_with_merging_with_removal(self):
        self.twopset1.remove('b')
        self.twopset2.remove('b')
        self.twopset2.remove('c')
        self.twopset1.merge(self.twopset2)
        self.twopset2.merge(self.twopset1)
        self.assertTrue(self.twopset1.query('a'))
        self.assertFalse(self.twopset1.query('b'))
        self.assertFalse(self.twopset1.query('c'))
        self.assertTrue(self.twopset1.query('d'))
        self.assertTrue(self.twopset2.query('a'))
        self.assertFalse(self.twopset2.query('b'))
        self.assertFalse(self.twopset2.query('c'))
        self.assertTrue(self.twopset2.query('d'))


if __name__ == '__main__':
    unittest.main()
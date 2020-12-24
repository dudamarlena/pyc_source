# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gg/PycharmProjects/gg-python3-crdt/build/lib/tests/test_sequence.py
# Compiled at: 2019-04-22 02:28:32
# Size of source mod 2**32: 5470 bytes
import unittest, uuid, set_sys_path
from sequence import Sequence
from datetime import datetime

class TestSequence(unittest.TestCase):

    def setUp(self):
        self.seq1 = Sequence(uuid.uuid4())
        self.seq2 = Sequence(uuid.uuid4())
        self.id1a = datetime.timestamp(datetime.now())
        self.seq1.add('a', self.id1a)
        self.id1b = datetime.timestamp(datetime.now())
        self.seq1.add('b', self.id1b)
        self.id2c = datetime.timestamp(datetime.now())
        self.seq2.add('c', self.id2c)
        self.id2b = datetime.timestamp(datetime.now())
        self.seq2.add('b', self.id2b)
        self.id2d = datetime.timestamp(datetime.now())
        self.seq2.add('d', self.id2d)

    def test_elements_add_correctly_sequence(self):
        self.assertEqual(self.seq1.get_seq(), 'ab')
        self.assertEqual(self.seq2.get_seq(), 'cbd')

    def test_querying_sequence_without_removal_and_merging(self):
        self.assertTrue(self.seq1.query(self.id1a))
        self.assertTrue(self.seq1.query(self.id1b))
        self.assertFalse(self.seq1.query(self.id2b))
        self.assertFalse(self.seq1.query(self.id2c))
        self.assertFalse(self.seq1.query(self.id2d))
        self.assertFalse(self.seq2.query(self.id1a))
        self.assertFalse(self.seq2.query(self.id1b))
        self.assertTrue(self.seq2.query(self.id2c))
        self.assertTrue(self.seq2.query(self.id2b))
        self.assertTrue(self.seq2.query(self.id2d))

    def test_merging_sequence_without_removal(self):
        self.seq1.merge(self.seq2)
        self.assertEqual(self.seq1.get_seq(), 'abcbd')
        self.seq2.merge(self.seq1)
        self.assertEqual(self.seq2.get_seq(), 'abcbd')
        self.assertEqual(self.seq1.get_seq(), self.seq2.get_seq())

    def test_querying_sequence_with_merging_without_removal(self):
        self.seq2.merge(self.seq1)
        self.assertTrue(self.seq2.query(self.id1a))
        self.assertTrue(self.seq2.query(self.id1b))
        self.assertTrue(self.seq2.query(self.id2c))
        self.assertTrue(self.seq2.query(self.id2b))
        self.assertTrue(self.seq2.query(self.id2d))
        self.seq1.merge(self.seq2)
        self.assertTrue(self.seq1.query(self.id1a))
        self.assertTrue(self.seq1.query(self.id1b))
        self.assertTrue(self.seq1.query(self.id2b))
        self.assertTrue(self.seq1.query(self.id2c))
        self.assertTrue(self.seq1.query(self.id2d))

    def test_elements_remove_correctly_sequence(self):
        self.seq1.remove(self.id1b)
        self.assertEqual(self.seq1.get_seq(), 'a')
        self.seq2.remove(self.id2b)
        self.seq2.remove(self.id2c)
        self.assertEqual(self.seq2.get_seq(), 'd')

    def test_querying_sequence_without_merging_with_removal(self):
        self.seq1.remove(self.id1b)
        self.assertTrue(self.seq1.query(self.id1a))
        self.assertFalse(self.seq1.query(self.id1b))
        self.assertFalse(self.seq1.query(self.id2b))
        self.assertFalse(self.seq1.query(self.id2c))
        self.assertFalse(self.seq1.query(self.id2d))
        self.seq2.remove(self.id2b)
        self.seq2.remove(self.id2c)
        self.assertFalse(self.seq2.query(self.id1a))
        self.assertFalse(self.seq2.query(self.id1b))
        self.assertFalse(self.seq2.query(self.id2b))
        self.assertFalse(self.seq2.query(self.id2c))
        self.assertTrue(self.seq2.query(self.id2d))

    def test_merging_sequence_with_removal(self):
        self.seq1.remove(self.id1b)
        self.seq2.remove(self.id2c)
        self.seq1.merge(self.seq2)
        self.assertEqual(self.seq1.get_seq(), 'abd')
        self.seq2.merge(self.seq1)
        self.assertEqual(self.seq2.get_seq(), 'abd')
        self.assertEqual(self.seq2.get_seq(), self.seq2.get_seq())

    def test_querying_sequence_with_merging_with_removal(self):
        self.seq1.remove(self.id1b)
        self.seq2.remove(self.id2c)
        self.seq1.merge(self.seq2)
        self.seq2.merge(self.seq1)
        self.assertTrue(self.seq1.query(self.id1a))
        self.assertFalse(self.seq1.query(self.id1b))
        self.assertTrue(self.seq1.query(self.id2b))
        self.assertFalse(self.seq1.query(self.id2c))
        self.assertTrue(self.seq1.query(self.id2d))
        self.assertTrue(self.seq2.query(self.id1a))
        self.assertFalse(self.seq2.query(self.id1b))
        self.assertTrue(self.seq2.query(self.id2b))
        self.assertFalse(self.seq2.query(self.id2c))
        self.assertTrue(self.seq2.query(self.id2d))


if __name__ == '__main__':
    unittest.main()
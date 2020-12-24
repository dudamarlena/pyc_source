# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bktree/test.py
# Compiled at: 2016-08-24 12:46:47
# Size of source mod 2**32: 651 bytes
import unittest, bktree

class BkTreeTest(unittest.TestCase):

    def test_gets_close_words(self):
        words = [
         254]
        tree = bktree.Tree(words)
        self.assertEqual([node.num for node in tree.search(255, 1)], [254])

    def test_finds_far_words(self):
        words = [
         1]
        tree = bktree.Tree(words)
        self.assertEqual([node.num for node in tree.search(255, 15)], [1])

    def test_empty_search(self):
        words = [
         254, 253, 251, 247, 239, 223, 191, 127]
        tree = bktree.Tree(words)
        self.assertEqual(tree.search(255, 0), [])


if __name__ == '__main__':
    unittest.main()
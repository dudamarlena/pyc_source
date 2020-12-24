# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/googlesafebrowsing/hashprefix_trie_test.py
# Compiled at: 2010-12-12 06:18:56
"""Unittest for googlesafebrowsing.hashprefix_trie."""
import hashprefix_trie, unittest

class HashPrefixTrieTest(unittest.TestCase):

    def assertSameElements(self, a, b):
        a = sorted(list(a))
        b = sorted(list(b))
        self.assertEqual(a, b)

    def testSimple(self):
        trie = hashprefix_trie.HashprefixTrie()
        trie.Insert('aabc', 1)
        trie.Insert('aabcd', 2)
        trie.Insert('acde', 3)
        trie.Insert('abcdefgh', 4)
        self.assertSameElements([1, 2], trie.GetPrefixMatches('aabcdefg'))
        self.assertSameElements([1, 2], trie.GetPrefixMatches('aabcd'))
        self.assertSameElements([1], trie.GetPrefixMatches('aabc'))
        self.assertSameElements([3], trie.GetPrefixMatches('acde'))
        self.assertEqual(4, trie.Size())
        trie.Delete('abcdefgh', 4)
        self.assertEqual(None, trie._GetNode('abcd'))
        trie.Delete('aabc', 2)
        trie.Delete('aaaa', 1)
        self.assertEqual(3, trie.Size())
        trie.Delete('aabc', 1)
        self.assertEqual(2, trie.Size())
        self.assertSameElements(['aabcd', 'acde'], trie.PrefixIterator())
        return


if __name__ == '__main__':
    unittest.main()
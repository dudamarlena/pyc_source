# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mueddit/tests/test.py
# Compiled at: 2019-04-19 02:33:56
# Size of source mod 2**32: 1524 bytes
import unittest
from mueddit import make_dawg, Iterator

class TestIterator(unittest.TestCase):

    def test_initial_final(self):
        dawg = make_dawg(('', 'a'))
        found = set(Iterator('b', 1, dawg))
        self.assertEqual({'', 'a'}, found)

    def test_foo(self):
        dawg = make_dawg(('foo', 'bar'))
        found = set(Iterator('baz', 1, dawg))
        self.assertEqual({'bar'}, found)
        found = set(Iterator('baz', 2, dawg))
        self.assertEqual({'bar'}, found)

    def test_this(self):
        dictionary = ('this', 'that', 'other')
        dawg = make_dawg(dictionary)
        found = set(Iterator('the', 1, dawg))
        self.assertEqual(set(), found)
        found = set(Iterator('the', 2, dawg))
        self.assertEqual(set(dictionary), found)

    def test_long_head(self):
        found = set(Iterator('abtrtz', 1, make_dawg(('abtrbtz', ))))
        self.assertEqual({'abtrbtz'}, found)

    def test_tolerance(self):
        dictionary = ('meter', 'otter', 'potter')
        dawg = make_dawg(dictionary)
        found = set(Iterator('mutter', 1, dawg))
        self.assertEqual(set(), found)
        found = set(Iterator('mutter', 2, dawg))
        self.assertEqual(set(dictionary), found)

    def test_binary(self):
        dictionary = ('ababa', 'babab')
        dawg = make_dawg(dictionary)
        found = set(Iterator('abba', 3, dawg))
        self.assertEqual(set(dictionary), found)


if __name__ == '__main__':
    unittest.main()
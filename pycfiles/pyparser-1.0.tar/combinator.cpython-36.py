# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/test/combinator.py
# Compiled at: 2015-11-14 12:09:33
# Size of source mod 2**32: 1625 bytes
import unittest
from parsec import *
simple = 'It is a simple string.'

class TestCombinator(unittest.TestCase):

    def test_many_0(self):
        st = BasicState(simple)
        p = many(one)
        re = p(st)
        data = ''.join(re)
        self.assertEqual(data, simple)

    def test_many_1(self):
        st = BasicState(simple)
        p = many(eq('I'))
        re = p(st)
        data = ''.join(re)
        self.assertEqual(data, 'I')

    def test_many_2(self):
        st = BasicState(simple)
        p = many(eq('z'))
        re = p(st)
        data = ''.join(re)
        self.assertEqual(data, '')

    def test_many0_1(self):
        st = BasicState(simple)
        p = many1(one)
        re = p(st)
        data = ''.join(re)
        self.assertEqual(data, simple)

    def test_many1_1(self):
        st = BasicState(simple)
        p = many1(eq('I'))
        re = p(st)
        data = ''.join(re)
        self.assertEqual(data, 'I')

    def test_many1_2(self):
        st = BasicState(simple)
        p = many1(eq('z'))
        with self.assertRaises(ParsecError):
            p(st)

    def test_sep_0(self):
        st = BasicState(simple)
        p = sep(many1(ne(' ')), eq(' '))
        re = p(st)
        data = [''.join(item) for item in re]
        self.assertEqual(data, simple.split(' '))

    def test_sep1_0(self):
        st = BasicState(simple)
        p = sep1(many1(ne(' ')), eq(' '))
        re = p(st)
        data = [''.join(item) for item in re]
        self.assertEqual(data, simple.split(' '))


if __name__ == '__main__':
    unittest.main()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/exedre/Dropbox/exedre@gmail.com/Dropbox/Work/GeCo-dev/infomedia-1.0/build/lib/infomedia/hash2cfg/test/simplefuncs.py
# Compiled at: 2012-07-20 17:39:58
import unittest, infomedia
from infomedia.hash2cfg import *

def td_intlist_test(s, *args, **kwargs):
    args_str = (', ').join([ '%r' % a for a in args ] + [ '%s=%r' % (k, v) for k, v in kwargs.iteritems() ])

    def test_generated(self):
        self.assertEqual(s, get_intlist(*args))

    test_generated.__doc__ = 'get_intlist(%s)' % args_str
    return test_generated


class SimpleFuncsTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_list_00(self):
        """get_list(None)"""
        self.assertEqual(None, get_list(None))
        return

    def test_get_list_01(self):
        """get_list('A,B,C,D')"""
        self.assertEqual(['A', 'B', 'C', 'D'], get_list('A,B,C,D'))

    def test_get_list_02(self):
        """get_list('A,B.C,D')"""
        self.assertEqual(['A', 'B.C', 'D'], get_list('A,B.C,D'))

    def test_get_list_03(self):
        """get_list('A,B.C,D',sep='.')"""
        self.assertEqual(['A,B', 'C,D'], get_list('A,B.C,D', sep='.'))

    def test_get_list_04(self):
        """get_list('A, B , C , D')"""
        self.assertEqual(['A', 'B', 'C', 'D'], get_list('A , B,   C   , D'))

    test_intlist_00 = td_intlist_test([1, 2, 3], '1 , 2 , 3')

    def test_explode_00(self):
        """explode_list('II$$','IT,FR,DE,UK')"""
        self.assertEqual(['IIIT', 'IIFR', 'IIDE', 'IIUK'], explode_list('II$$', 'IT,FR,DE,UK'))

    def test_explode_01(self):
        """explode_list('$$','IT,FR,DE,UK')"""
        self.assertNotEqual(['IIIT', 'IIFR', 'IIDE', 'IIUK'], explode_list('$$', 'IT,FR,DE,UK'))


if __name__ == '__main__':
    unittest.main()
__all__ = ['SimpleFuncsTest']
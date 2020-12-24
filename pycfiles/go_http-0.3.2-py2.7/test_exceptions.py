# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/go_http/tests/test_exceptions.py
# Compiled at: 2017-02-17 10:13:07
"""
Tests for go_http.exceptions.
"""
from unittest import TestCase
from go_http.exceptions import PagedException

class TestPagedException(TestCase):

    def test_creation(self):
        err = ValueError('Testing Error')
        p = PagedException('12345', err)
        self.assertTrue(isinstance(p, Exception))
        self.assertEqual(p.cursor, '12345')
        self.assertEqual(p.error, err)

    def test_repr(self):
        p = PagedException('abcde', ValueError('Test ABC'))
        self.assertEqual(repr(p), "<PagedException cursor=u'abcde' error=ValueError('Test ABC',)>")

    def test_str(self):
        p = PagedException('lmnop', ValueError('Test LMN'))
        self.assertEqual(str(p), "<PagedException cursor=u'lmnop' error=ValueError('Test LMN',)>")
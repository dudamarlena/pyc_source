# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/out_of_shape/test_strutil.py
# Compiled at: 2018-01-06 14:43:43
import unittest
from pyutil.assertutil import _assert
from pyutil import strutil

class Teststrutil(unittest.TestCase):

    def test_short_input(self):
        self.failUnless(strutil.pop_trailing_newlines('\r\n') == '')
        self.failUnless(strutil.pop_trailing_newlines('\r') == '')
        self.failUnless(strutil.pop_trailing_newlines('x\r\n') == 'x')
        self.failUnless(strutil.pop_trailing_newlines('x\r') == 'x')

    def test_split(self):
        _assert(strutil.split_on_newlines('x\r\ny') == ['x', 'y'], strutil.split_on_newlines('x\r\ny'))
        _assert(strutil.split_on_newlines('x\r\ny\r\n') == ['x', 'y', ''], strutil.split_on_newlines('x\r\ny\r\n'))
        _assert(strutil.split_on_newlines('x\n\ny\n\n') == ['x', '', 'y', '', ''], strutil.split_on_newlines('x\n\ny\n\n'))

    def test_commonprefix(self):
        _assert(strutil.commonprefix(['foo', 'foobarooo', 'foosplat']) == 'foo', strutil.commonprefix(['foo', 'foobarooo', 'foosplat']))
        _assert(strutil.commonprefix(['foo', 'afoobarooo', 'foosplat']) == '', strutil.commonprefix(['foo', 'afoobarooo', 'foosplat']))

    def test_commonsuffix(self):
        _assert(strutil.commonsuffix(['foo', 'foobarooo', 'foosplat']) == '', strutil.commonsuffix(['foo', 'foobarooo', 'foosplat']))
        _assert(strutil.commonsuffix(['foo', 'foobarooo', 'foosplato']) == 'o', strutil.commonsuffix(['foo', 'foobarooo', 'foosplato']))
        _assert(strutil.commonsuffix(['foo', 'foobarooofoo', 'foosplatofoo']) == 'foo', strutil.commonsuffix(['foo', 'foobarooofoo', 'foosplatofoo']))
# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/halfak/env/3.4/lib/python3.4/site-packages/mysqltsv/tests/test_functions.py
# Compiled at: 2015-07-11 11:35:13
# Size of source mod 2**32: 633 bytes
from nose.tools import eq_
from ..functions import decode, encode

def test_encode():
    eq_(encode('foobar'), 'foobar')
    eq_(encode(5), '5')
    eq_(encode(b'foobar'), 'foobar')
    eq_(encode('foo\tbar'), 'foo\\tbar')


def test_decode():
    eq_(decode('foobar'), 'foobar')
    eq_(decode('5'), '5')
    eq_(decode('5', int), 5)
    eq_(decode(b'foobar'), 'foobar')
    eq_(decode('foo\\tbar\\n'), 'foo\tbar\n')


def test_encode_decode():
    input = '\t\nfoobar\t,derp'
    expected_encoded = '\\t\\nfoobar\\t,derp'
    eq_(encode(input), expected_encoded)
    eq_(decode(encode(input)), input)
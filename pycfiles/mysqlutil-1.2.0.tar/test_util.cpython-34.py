# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/halfak/env/3.4/lib/python3.4/site-packages/mysqltsv/tests/test_util.py
# Compiled at: 2016-01-30 13:14:28
# Size of source mod 2**32: 810 bytes
from nose.tools import eq_
from ..util import decode, encode, read_row

def test_encode():
    eq_(encode('foobar'), 'foobar')
    eq_(encode(5), '5')
    eq_(encode('foobar'), 'foobar')
    eq_(encode('foo\tbar'), 'foo\\tbar')


def test_decode():
    eq_(decode('foobar'), 'foobar')
    eq_(decode('5'), '5')
    eq_(decode('5', int), 5)
    eq_(decode('foobar'), 'foobar')
    eq_(decode('foo\\tbar\\n'), 'foo\tbar\n')


def test_encode_decode():
    input = '\t\nfoobar\t,derp'
    expected_encoded = '\\t\\nfoobar\\t,derp'
    eq_(encode(input), expected_encoded)
    eq_(decode(encode(input)), input)


def test_read_row():
    eq_(list(read_row('foo\tbar\tNULL')), ['foo', 'bar', None])
    eq_(list(read_row('foo\t12\tNULL', types=[str, int, str])), [
     'foo', 12, None])
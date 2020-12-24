# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/halfak/env/3.4/lib/python3.4/site-packages/mysqltsv/tests/test_row_type.py
# Compiled at: 2016-01-30 13:35:26
# Size of source mod 2**32: 810 bytes
import pickle
from nose.tools import eq_
from ..row_type import RowGenerator

def test_row_type():
    MyRow = RowGenerator(['foo', 'bar', 'baz'])
    r = MyRow('15\t16\tNULL')
    eq_(r.foo, '15')
    eq_(r['foo'], '15')
    eq_(r[0], '15')
    eq_(r.bar, '16')
    eq_(r['bar'], '16')
    eq_(r[1], '16')
    eq_(r.baz, None)
    eq_(r['baz'], None)
    eq_(r[2], None)
    MyRow = RowGenerator(['foo', 'bar', 'baz'], types=[int, int, int])
    r = MyRow('15\t16\tNULL')
    eq_(r.foo, 15)
    eq_(r['foo'], 15)
    eq_(r[0], 15)
    eq_(r.bar, 16)
    eq_(r['bar'], 16)
    eq_(r[1], 16)
    eq_(r.baz, None)
    eq_(r['baz'], None)
    eq_(r[2], None)
    eq_(pickle.loads(pickle.dumps(r)).baz, None)
    eq_(pickle.loads(pickle.dumps(r))['baz'], None)
    eq_(pickle.loads(pickle.dumps(r))[2], None)
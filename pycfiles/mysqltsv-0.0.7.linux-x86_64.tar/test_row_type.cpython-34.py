# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
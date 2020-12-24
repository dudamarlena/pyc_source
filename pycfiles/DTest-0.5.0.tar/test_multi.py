# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/klmitch/devel/src/dtest/tests/test_multi.py
# Compiled at: 2011-06-29 14:07:37
from dtest import *
from dtest.util import *

@repeat(2)
def test_multi():
    recorded = []

    def inner(*args, **kwargs):
        recorded.append((args, kwargs))

    yield (
     'inner1', inner, (1, ), dict(kw=1))
    yield (
     'inner2', inner, (2, ), dict(kw=2))
    assert_equal(len(recorded), 4)
    assert_tuple_equal(recorded[0][0], (1, ))
    assert_dict_equal(recorded[0][1], dict(kw=1))
    assert_tuple_equal(recorded[1][0], (1, ))
    assert_dict_equal(recorded[1][1], dict(kw=1))
    assert_tuple_equal(recorded[2][0], (2, ))
    assert_dict_equal(recorded[2][1], dict(kw=2))
    assert_tuple_equal(recorded[3][0], (2, ))
    assert_dict_equal(recorded[3][1], dict(kw=2))
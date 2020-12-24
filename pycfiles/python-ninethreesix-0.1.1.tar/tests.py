# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/brad/python-nine-three-six/ninethreesix/tests.py
# Compiled at: 2015-04-04 13:10:11
from nose.tools import eq_
from .password import Password

def test_init():
    p = Password()
    eq_(p.num_words, 3)
    eq_(p.min_len, 3)
    eq_(p.max_len, 6)
    eq_(p.content.find('\n'), -1)


def test_password():
    p = Password()
    result = p.password()
    eq_(type(result), list)
    eq_(len(result), 3)


def test_as_string():
    p = Password()
    result = p.as_string()
    eq_(type(result), str)
    eq_(result.count('-'), 2)
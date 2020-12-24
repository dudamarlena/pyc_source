# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/tests/test_number.py
# Compiled at: 2019-01-13 18:15:47
# Size of source mod 2**32: 342 bytes
from parsr import Number

def test_zero():
    assert Number('0') == 0.0


def test_positive_integer():
    assert Number('123') == 123.0


def test_negative_integer():
    assert Number('-123') == -123.0


def test_positive_float():
    assert Number('123.97') == 123.97


def test_negative_float():
    assert Number('-123.97') == -123.97
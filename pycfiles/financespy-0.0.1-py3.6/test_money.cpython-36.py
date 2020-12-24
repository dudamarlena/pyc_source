# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_money.py
# Compiled at: 2019-06-26 15:43:38
# Size of source mod 2**32: 825 bytes
import pytest
from financespy import Money

def test_simple_sum():
    m1 = Money(0.1)
    m2 = Money(0.2)
    assert Money(0.3) == m1 + m2


def test_overflow():
    m1 = Money(1e+20)
    m2 = Money(100)
    assert Money('100000000000000000100') == m1 + m2


def test_difference():
    result = Money('84.6')
    if not Money(100) - Money(15.4) == result:
        raise AssertionError
    else:
        assert 100 - Money(15.4) == result
        assert Money(100.0) - 15.4 == result


def test_multiplication():
    assert Money(15) * 4 == Money(60)
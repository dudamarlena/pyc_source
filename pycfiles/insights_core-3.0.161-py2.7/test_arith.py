# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsr/examples/tests/test_arith.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsr.examples.arith import evaluate

def test_single_ops():
    assert evaluate('2+3') == 5
    assert evaluate('1-3') == -2
    assert evaluate('2*3') == 6
    assert evaluate('4/2') == 2


def test_multiple_ops():
    assert evaluate('2+3+4') == 9
    assert evaluate('1-3+2') == 0
    assert evaluate('2*3*4') == 24
    assert evaluate('3*4/2') == 6


def test_nested():
    assert evaluate('24-2*(3+4)') == 10


def test_spaces():
    assert evaluate('24 - 2 * ( 3 + 4 )') == 10
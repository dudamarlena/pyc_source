# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsr/tests/test_boolean.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsr import Char

def test_and():
    p = Char('a') + Char('b')
    assert p('ab') == ['a', 'b']


def test_or():
    p = Char('a') | Char('b')
    assert p('a') == 'a'
    assert p('b') == 'b'
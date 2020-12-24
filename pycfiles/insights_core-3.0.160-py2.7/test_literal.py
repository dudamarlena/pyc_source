# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsr/tests/test_literal.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsr import Literal

def test_literal():
    p = Literal('123')
    assert p('123') == '123'


def test_literal_value():
    p = Literal('true', value=True)
    assert p('true') is True


def test_literal_ignore_case():
    p = Literal('true', ignore_case=True)
    assert p('TrUe') == 'TrUe'


def test_literal_value_ignore_case():
    p = Literal('true', value=True, ignore_case=True)
    assert p('TRUE') is True
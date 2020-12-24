# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsr/tests/test_keep.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsr import Colon, QuotedString

def test_keepleft():
    key = QuotedString << Colon
    assert key('"key":') == 'key'
    key = Colon << QuotedString
    assert key(':"key"') == ':'


def test_keepright():
    key = QuotedString >> Colon
    assert key('"key":') == ':'
    key = Colon >> QuotedString
    assert key(':"key"') == 'key'


def test_middle():
    key = Colon >> QuotedString << Colon
    assert key(':"key":') == 'key'
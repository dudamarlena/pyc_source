# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsr/tests/test_string.py
# Compiled at: 2019-11-14 13:57:46
import string
from insights.parsr import InSet, String, DoubleQuotedString, QuotedString

def test_inset():
    assert InSet('abc', 'set of abc')('a') == 'a'


def test_string():
    sb = String(string.ascii_letters)
    data = 'abcde'
    assert sb(data) == 'abcde'


def test_quoted_string():
    data = "'abcde'"
    assert QuotedString(data) == 'abcde'


def test_escaped_string():
    data = ('\n    "%h %l %u %t \\"%r\\" %>s %b \\"%{Referer}i\\" \\"%{User-Agent}i\\""\n    ').strip()
    assert DoubleQuotedString(data)
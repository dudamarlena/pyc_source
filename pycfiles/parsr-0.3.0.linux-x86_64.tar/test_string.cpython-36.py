# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/tests/test_string.py
# Compiled at: 2019-01-13 18:16:37
# Size of source mod 2**32: 513 bytes
import string
from parsr import InSet, String, DoubleQuotedString, QuotedString

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
    data = '\n    "%h %l %u %t \\"%r\\" %>s %b \\"%{Referer}i\\" \\"%{User-Agent}i\\""\n    '.strip()
    assert DoubleQuotedString(data)
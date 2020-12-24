# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_utils.py
# Compiled at: 2013-07-27 09:03:17
from pymills.utils import notags

def test_notags():
    s = '<html>foo</html>'
    x = notags(s)
    assert x == 'foo'
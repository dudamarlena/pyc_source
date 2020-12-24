# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_utils.py
# Compiled at: 2013-07-27 09:03:17
from pymills.utils import notags

def test_notags():
    s = '<html>foo</html>'
    x = notags(s)
    assert x == 'foo'
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/buildutils/test/test_compat.py
# Compiled at: 2007-08-08 19:57:13
"""Unit tests for the buildutils.compat package."""

def test_string_template():
    from buildutils.compat.string_template import Template
    actual = Template('hello ${who}').substitute({'who': 'world'})
    expected = 'hello world'
    assert actual == expected
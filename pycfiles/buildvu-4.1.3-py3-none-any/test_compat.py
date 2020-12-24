# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/buildutils/test/test_compat.py
# Compiled at: 2007-08-08 19:57:13
__doc__ = 'Unit tests for the buildutils.compat package.'

def test_string_template():
    from buildutils.compat.string_template import Template
    actual = Template('hello ${who}').substitute({'who': 'world'})
    expected = 'hello world'
    assert actual == expected
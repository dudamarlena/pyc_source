# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyweb-plugins/register/test/test_compile.py
# Compiled at: 2009-12-06 12:52:40


def test_compile():
    try:
        import tiddlywebplugins.register
        assert True
    except ImportError, exc:
        assert False, exc
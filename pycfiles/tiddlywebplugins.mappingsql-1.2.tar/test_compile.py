# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyweb-plugins/mappingsqlstore/test/test_compile.py
# Compiled at: 2010-02-01 16:05:20


def test_compile():
    try:
        import tiddlywebplugins.mappingsql
        assert True
    except ImportError, exc:
        assert False, exc
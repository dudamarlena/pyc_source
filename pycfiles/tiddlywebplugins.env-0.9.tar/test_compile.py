# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyweb-plugins/env/test/test_compile.py
# Compiled at: 2010-03-14 09:28:49


def test_compile():
    try:
        import tiddlywebplugins.env
        assert True
    except ImportError, exc:
        assert False, exc
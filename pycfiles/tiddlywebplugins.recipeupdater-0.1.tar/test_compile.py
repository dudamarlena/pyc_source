# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyweb-plugins/recipeupdater/test/test_compile.py
# Compiled at: 2010-08-25 06:24:33


def test_compile():
    try:
        import tiddlywebplugins.recipeupdater
        assert True
    except ImportError, exc:
        assert False, exc
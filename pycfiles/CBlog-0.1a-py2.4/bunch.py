# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cblog/utils/bunch.py
# Compiled at: 2006-12-06 04:38:03


class Bunch(dict):
    __module__ = __name__

    def __init__(self, **kw):
        dict.__init__(self, kw)
        self.__dict__.update(kw)
# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cblog/utils/bunch.py
# Compiled at: 2006-12-06 04:38:03


class Bunch(dict):
    __module__ = __name__

    def __init__(self, **kw):
        dict.__init__(self, kw)
        self.__dict__.update(kw)
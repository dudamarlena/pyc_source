# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmlstruct/errorbag.py
# Compiled at: 2008-10-01 11:16:13
import string

class ErrorBag:
    __module__ = __name__

    def __init__(self):
        self.__errors = []

    def addError(self, descr, ctx):
        self.__errors.append((descr, ctx))

    def clear(self):
        self.__errors = []

    def length(self):
        return len(self.__errors)

    def __str__(self):
        l = []
        for (descr, ctx) in self.__errors:
            l.append(ctx + ': ' + descr)

        return string.join(l, '\n')
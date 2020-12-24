# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\textconverter\method_missing.py
# Compiled at: 2011-07-18 08:02:42


class MethodMissing(object):

    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:

            def method(*args, **kw):
                return self.method_missing(name, *args, **kw)

            return method

    def method_missing(self, name, *args, **kw):
        raise AttributeError, name
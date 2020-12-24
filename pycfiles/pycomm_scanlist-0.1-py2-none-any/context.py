# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pycommunicate\proxies\context.py
# Compiled at: 2016-06-12 12:34:46


class CallCTX:

    def __init__(self, **exposed):
        self.__stuff = exposed
        self.__active = True

    def use(self, name):
        if self.__active:
            return self.__stuff[name]
        else:
            return

    def deactivate(self):
        self.__stuff = {}
        self.__active = False
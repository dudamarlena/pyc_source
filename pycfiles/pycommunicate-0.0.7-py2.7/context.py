# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
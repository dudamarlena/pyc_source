# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpsim/error.py
# Compiled at: 2018-12-30 10:46:50


class SnmpsimError(Exception):
    __module__ = __name__


class NoDataNotification(SnmpsimError):
    __module__ = __name__


class MoreDataNotification(SnmpsimError):
    __module__ = __name__

    def __init__(self, **kwargs):
        self.__kwargs = kwargs

    def __contains__(self, key):
        return key in self.__kwargs

    def __getitem__(self, key):
        return self.__kwargs[key]

    def get(self, key):
        return self.__kwargs.get(key)

    def keys(self):
        return self.__kwargs.keys()
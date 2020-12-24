# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/infomedia/patterns.py
# Compiled at: 2012-08-05 09:11:54


class Borg(object):
    _state = {}

    def __new__(cls, *p, **k):
        self = object.__new__(cls, *p, **k)
        self.__dict__ = cls._state
        return self


class Singleton(object):

    def __new__(type):
        if '_the_instance' not in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance


__all__ = ('\n Borg\n Singleton\n').split()
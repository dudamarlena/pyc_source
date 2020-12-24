# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jlopes/PycharmProjects/mcg/core/db/Singleton.py
# Compiled at: 2017-01-24 01:10:58
# Size of source mod 2**32: 534 bytes


class Singleton(type):

    def __init__(cls, name, bases, dic):
        type.__init__(cls, name, bases, dic)

        def __copy__(self):
            return self

        def __deepcopy__(self, memo=None):
            return self

        cls.__copy__ = __copy__
        cls.__deepcopy__ = __deepcopy__

    def __call__(cls, *args, **kwargs):
        try:
            return cls._Singleton__instance
        except AttributeError:
            cls._Singleton__instance = super(Singleton, cls).__call__(*args, **kwargs)
            return cls._Singleton__instance
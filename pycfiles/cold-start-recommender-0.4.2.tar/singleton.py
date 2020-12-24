# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mal/pCloud/Python/cold-start-recommender/csrec/tools/singleton.py
# Compiled at: 2017-12-01 12:35:53


class Singleton(object):
    __instance = {}

    def __new__(cls, *args, **kwargs):
        if Singleton.__instance.get(cls) is None:
            cls.__original_init__ = cls.__init__
            Singleton.__instance[cls] = object.__new__(cls, *args, **kwargs)
        elif cls.__init__ == cls.__original_init__:

            def nothing(*args, **kwargs):
                pass

            cls.__init__ = nothing
        return Singleton.__instance[cls]
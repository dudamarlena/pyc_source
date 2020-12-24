# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
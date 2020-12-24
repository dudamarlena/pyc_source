# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/subaligner/singleton.py
# Compiled at: 2020-01-25 08:37:53
# Size of source mod 2**32: 441 bytes


class _Singleton(type):
    __doc__ = ' A metaclass that creates a Singleton base class when called. '
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = (super(_Singleton, cls).__call__)(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    pass
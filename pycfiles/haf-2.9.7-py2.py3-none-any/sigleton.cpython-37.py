# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: J:\workspace\python\haf\haf\common\sigleton.py
# Compiled at: 2020-03-21 04:56:32
# Size of source mod 2**32: 1225 bytes
"""
file name : sigleton
description : the sigleton defined
others:
    usage:
    1, class A(metaclass=SingletonType):
    2, class B(Singleton)
    3, @sigleton
       class C(object):

"""

class SingletonType(type):

    def __init__(self, *args, **kwargs):
        self._SingletonType__instance = None
        (super(SingletonType, self).__init__)(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self._SingletonType__instance is None:
            self._SingletonType__instance = (super(SingletonType, self).__call__)(*args, **kwargs)
        return self._SingletonType__instance


def singleton(cls):
    __instance = {}

    def _wraps(*args, **kwargs):
        if cls not in __instance:
            __instance[cls] == cls(*args, **kwargs)
        return __instance[cls]

    return _wraps


class Singleton(object):
    import threading
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with Singleton._lock:
                if not hasattr(cls, '_instance'):
                    Singleton._instance = super().__new__(cls)
        return Singleton._instance
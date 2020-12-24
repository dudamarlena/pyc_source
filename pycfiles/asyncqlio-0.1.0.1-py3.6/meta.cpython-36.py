# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncqlio/meta.py
# Compiled at: 2017-11-29 06:02:28
# Size of source mod 2**32: 2698 bytes
"""
Useful metamagic classes, such as async ABCs.
"""
import inspect
from abc import ABCMeta

def make_proxy(name: str):
    """
    Makes a proxy object for magic methods.
    """

    def proxy(self, *args, **kwargs):
        item = self.__getattr__(name)
        return item(*args, **kwargs)

    return proxy


def proxy_to_getattr(*magic_methods: str):
    """
    Proxies a method to to ``__getattr__`` when it would not be normally proxied.

    This is used for magic methods that are slot loaded (``__setattr__`` etc.)

    :param magic_methods: The magic methods to proxy to getattr.
    """

    def _modify_type(obb):
        for item in magic_methods:
            setattr(obb, item, make_proxy(item))

        return obb

    return _modify_type


class AsyncABCMeta(ABCMeta):
    __doc__ = '\n    Metaclass that gives all of the features of an abstract base class, but\n    additionally enforces coroutine correctness on subclasses. If any method\n    is defined as a coroutine in a parent, it must also be defined as a\n    coroutine in any child.\n    '

    def __init__(cls, name, bases, methods):
        coros = {}
        for base in reversed(cls.__mro__):
            coros.update((name, val) for name, val in vars(base).items() if inspect.iscoroutinefunction(val))

        for name, val in vars(cls).items():
            if name in coros and not inspect.iscoroutinefunction(val):
                raise TypeError('Must use async def %s%s' % (name, inspect.signature(val)))

        super().__init__(name, bases, methods)


class AsyncABC(metaclass=AsyncABCMeta):
    pass


class AsyncInstanceType(AsyncABCMeta):
    __doc__ = '\n    Metaclass that allows for asynchronous instance initialization and the\n    __init__() method to be defined as a coroutine.   Usage:\n    class Spam(metaclass=AsyncInstanceType):\n        async def __init__(self, x, y):\n            self.x = x\n            self.y = y\n    async def main():\n         s = await Spam(2, 3)\n         ...\n    '

    @staticmethod
    def __new__(meta, clsname, bases, attributes):
        if '__init__' in attributes:
            if not inspect.iscoroutinefunction(attributes['__init__']):
                raise TypeError('__init__ must be a coroutine')
        return super().__new__(meta, clsname, bases, attributes)

    async def __call__(cls, *args, **kwargs):
        self = (cls.__new__)(cls, *args, **kwargs)
        await (self.__init__)(*args, **kwargs)
        return self


class AsyncObject(metaclass=AsyncInstanceType):
    pass
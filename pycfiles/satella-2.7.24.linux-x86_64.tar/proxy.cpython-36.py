# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/structures/proxy.py
# Compiled at: 2020-05-12 15:04:16
# Size of source mod 2**32: 4933 bytes
import logging, typing as tp
T = tp.TypeVar('T')
logger = logging.getLogger(__name__)
_SETTABLE_KEYS = {
 '_Proxy__obj', '_Proxy__wrap_operations'}

class Proxy(tp.Generic[T]):
    __doc__ = '\n    A base class for classes that try to emulate some other object.\n\n    They will intercept all calls and place them on the target object.\n\n    Note that in-place operations will return the Proxy itself, whereas simple addition will shed\n    this proxy, returning object wrapped plus something.\n\n    Note that proxies are considered to be the type of the object that they wrap,\n    as well as considered to be of type Proxy.\n\n    :param object_to_wrap: object to wrap\n    :param wrap_operations: whether results of operations returning something else should be\n        also proxied. This will be done by the following code:\n        >>> a = a.__add__(b)\n        >>> return self.__class__(a)\n        Wrapped operations include ONLY add, sub, mul, all kinds of div.\n        If you want logical operations wrapped, file an issue.\n    '
    __slots__ = ('__obj', '__wrap_operations')

    def __init__(self, object_to_wrap: T, wrap_operations: bool=False):
        self._Proxy__obj = object_to_wrap
        self._Proxy__wrap_operations = wrap_operations

    def __call__(self, *args, **kwargs):
        return (self._Proxy__obj)(*args, **kwargs)

    def __getitem__(self, item):
        return self._Proxy__obj[item]

    def __setitem__(self, key, value):
        self._Proxy__obj[key] = value

    def __delitem__(self, key):
        del self._Proxy__obj[key]

    def __setattr__(self, key, value):
        if key in _SETTABLE_KEYS:
            super().__setattr__(key, value)
        else:
            setattr(self._Proxy__obj, key, value)

    def __getattr__(self, item):
        return getattr(self._Proxy__obj, item)

    def __delattr__(self, item):
        delattr(self._Proxy__obj, item)

    def __int__(self):
        return int(self._Proxy__obj)

    def __float__(self):
        return float(self._Proxy__obj)

    def __complex__(self):
        return complex(self._Proxy__obj)

    def __str__(self):
        return str(self._Proxy__obj)

    def __add__(self, other):
        result = self._Proxy__obj + other
        if self._Proxy__wrap_operations:
            result = self.__class__(result)
        return result

    def __iadd__(self, other):
        self._Proxy__obj += other
        return self

    def __sub__(self, other):
        result = self._Proxy__obj - other
        if self._Proxy__wrap_operations:
            result = self.__class__(result)
        return result

    def __isub__(self, other):
        self._Proxy__obj -= other
        return self

    def __mul__(self, other):
        result = self._Proxy__obj * other
        if self._Proxy__wrap_operations:
            result = self.__class__(result)
        return result

    def __divmod__(self, other):
        result = divmod(self._Proxy__obj, other)
        if self._Proxy__wrap_operations:
            result = self.__class__(result)
        return result

    def __floordiv__(self, other):
        result = self._Proxy__obj // other
        if self._Proxy__wrap_operations:
            result = self.__class__(result)
        return result

    def __truediv__(self, other):
        result = self._Proxy__obj / other
        if self._Proxy__wrap_operations:
            result = self.__class__(result)
        return result

    def __imul__(self, other):
        self._Proxy__obj *= other
        return self

    def __itruediv__(self, other):
        self.obj /= other
        return self

    def __ifloordiv__(self, other):
        self.obj //= other
        return self

    def __ilshift__(self, other):
        self.obj <<= other
        return self

    def __irshift__(self, other):
        self.obj >>= other
        return self

    def __iter__(self):
        return iter(self._Proxy__obj)

    def __len__(self):
        return len(self._Proxy__obj)

    def __contains__(self, item):
        return item in self._Proxy__obj

    def __hash__(self):
        return hash(self._Proxy__obj)

    def __eq__(self, other):
        return self._Proxy__obj == other

    def __or__(self, other):
        return self._Proxy__obj or other

    def __and__(self, other):
        return self._Proxy__obj and other

    def __le__(self, other):
        return self._Proxy__obj <= other

    def __lt__(self, other):
        return self._Proxy__obj < other

    def __ge__(self, other):
        return self._Proxy__obj >= other

    def __gt__(self, other):
        return self._Proxy__obj > other

    def __enter__(self):
        return self._Proxy__obj.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._Proxy__obj.__exit__(exc_type, exc_val, exc_tb)

    def __repr__(self):
        return repr(self._Proxy__obj)

    def __abs__(self):
        return abs(self._Proxy__obj)

    def __bool__(self):
        return bool(self._Proxy__obj)

    def __format__(self, format_spec):
        return self._Proxy__obj.__format__(format_spec)

    def __next__(self):
        return next(self._Proxy__obj)

    def __xor__(self, other):
        return self._Proxy__obj ^ other
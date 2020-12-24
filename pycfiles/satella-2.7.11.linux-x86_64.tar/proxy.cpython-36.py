# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/structures/proxy.py
# Compiled at: 2020-04-22 08:35:40
# Size of source mod 2**32: 3533 bytes
import logging, typing as tp
logger = logging.getLogger(__name__)
T = tp.TypeVar('T')

class Proxy(tp.Generic[T]):
    __doc__ = '\n    A base class for classes that try to emulate some other object.\n\n    They will intercept all calls and place them on the target object.\n\n    Note that in-place operations will return the Proxy itself, whereas simple addition will shed\n    this proxy, returning object wrapped plus something.\n    '
    __slots__ = ('__obj', )

    def __init__(self, object_to_wrap: T):
        self._Proxy__obj = object_to_wrap

    def __call__(self, *args, **kwargs):
        return (self._Proxy__obj)(*args, **kwargs)

    def __getitem__(self, item):
        return self._Proxy__obj[item]

    def __setitem__(self, key, value):
        self._Proxy__obj[key] = value

    def __delitem__(self, key):
        del self._Proxy__obj[key]

    def __setattr__(self, key, value):
        if key in ('_Proxy__obj', ):
            super().__setattr__(key, value)
        else:
            setattr(self._Proxy__obj, key, value)

    def __getattr__(self, item):
        return getattr(self._Proxy__obj, item)

    def __delattr__(self, item):
        del self._Proxy__obj[item]

    def __int__(self):
        return int(self._Proxy__obj)

    def __float__(self):
        return float(self._Proxy__obj)

    def __complex__(self):
        return complex(self._Proxy__obj)

    def __str__(self):
        return str(self._Proxy__obj)

    def __add__(self, other):
        return self._Proxy__obj + other

    def __iadd__(self, other):
        self._Proxy__obj += other
        return self

    def __sub__(self, other):
        return self._Proxy__obj - other

    def __isub__(self, other):
        self._Proxy__obj -= other
        return self

    def __mul__(self, other):
        return self._Proxy__obj * other

    def __divmod__(self, other):
        return divmod(self._Proxy__obj, other)

    def __floordiv__(self, other):
        return self._Proxy__obj // other

    def __truediv__(self, other):
        return self._Proxy__obj / other

    def __imul__(self, other):
        self._Proxy__obj * other
        return self

    def __itruediv__(self, other):
        self.obj / other
        return self

    def __ifloordiv__(self, other):
        self.obj //= other
        return self

    def __ilshift__(self, other):
        self.obj << other
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
        return self._Proxy__obj or other

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
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/concurrent/atomic.py
# Compiled at: 2020-05-12 15:04:16
# Size of source mod 2**32: 1549 bytes
import typing as tp
from .monitor import Monitor
Number = tp.Union[(int, float)]

class AtomicNumber(Monitor):
    __doc__ = "\n    An atomic number. Note that the class is not hashable and for a reason, since it's value\n    might change in time. So in this case this is more of like a container for numbers.\n\n    Treat it like a normal number, except all operations are executed atomically.\n    "
    __slots__ = ('value', )

    def __init__(self, v=0):
        super().__init__()
        self.value = v

    @Monitor.synchronized
    def __iadd__(self, other: Number) -> 'AtomicNumber':
        self.value += other
        return self

    @Monitor.synchronized
    def __isub__(self, other: int) -> 'AtomicNumber':
        self.value -= other
        return self

    @Monitor.synchronized
    def __imul__(self, other: int) -> 'AtomicNumber':
        self.value *= other
        return self

    @Monitor.synchronized
    def __eq__(self, other: tp.Union[('AtomicNumber', Number)]) -> bool:
        if isinstance(other, AtomicNumber):
            with Monitor.acquire(other):
                return self.value == other.value
        else:
            return self.value == other

    @Monitor.synchronized
    def __int__(self) -> int:
        return int(self.value)

    @Monitor.synchronized
    def __float__(self) -> float:
        return float(self.value)

    @Monitor.synchronized
    def __bool__(self) -> bool:
        return bool(self.value)

    @Monitor.synchronized
    def __abs__(self) -> Number:
        return abs(self.value)
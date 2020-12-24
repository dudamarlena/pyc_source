# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/medusa/counter.py
# Compiled at: 2019-04-05 17:19:18
# Size of source mod 2**32: 1508 bytes
from supervisor.compat import long

class counter:
    __doc__ = 'general-purpose counter'

    def __init__(self, initial_value=0):
        self.value = initial_value

    def increment(self, delta=1):
        result = self.value
        try:
            self.value = self.value + delta
        except OverflowError:
            self.value = long(self.value) + delta
        else:
            return result

    def decrement(self, delta=1):
        result = self.value
        try:
            self.value = self.value - delta
        except OverflowError:
            self.value = long(self.value) - delta
        else:
            return result

    def as_long(self):
        return long(self.value)

    def __nonzero__(self):
        return self.value != 0

    __bool__ = __nonzero__

    def __repr__(self):
        return '<counter value=%s at %x>' % (self.value, id(self))

    def __str__(self):
        s = str(long(self.value))
        if s[-1:] == 'L':
            s = s[:-1]
        return s
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ulutil/scale.py
# Compiled at: 2014-12-19 21:47:21
import math, types, numbers, bisect, numpy as np

def is_iterable(x):
    try:
        iter(x)
        return True
    except TypeError:
        return False


class quantitative(object):
    """Implement abstract quantitative scale."""

    def __init__(self, *args):
        self._domain = [
         0, 1]
        self._range = [0, 1]
        self._transform = lambda x: x
        self._inverse = lambda y: y
        self.domain(*args)

    def _in_domain(self, x):
        return x >= min(self._domain) and x <= max(self._domain)

    def _in_range(self, y):
        return y >= min(self._range) and y <= max(self._range)

    def __call__(self, x):
        if not self._in_domain(x):
            raise ValueError, 'outside domain'
        segment = bisect.bisect_right(self._domain, x) - 1
        if segment + 1 == len(self._domain):
            segment -= 1
        return (self._transform(x) - self._transform(self._domain[segment])) / (self._transform(self._domain[(segment + 1)]) - self._transform(self._domain[segment])) * (self._range[(segment + 1)] - self._range[segment]) + self._range[segment]

    def domain(self, *args):
        if len(args) == 0:
            return self._domain
        if is_iterable(args[0]):
            if len(args[0]) < 2:
                raise ValueError, 'domain specification needs at least two numbers'
            self._domain = [
             np.min(args[0]), np.max(args[0])]
        else:
            if len(args) != len(set(args)):
                raise ValueError, 'domain values must be unique'
            if list(args) != sorted(list(args)) and list(args)[::-1] != sorted(list(args)):
                raise ValueError, 'domain values must be sorted'
            self._domain = args
        self._domain = map(float, self._domain)
        map(self._transform, self._domain)
        return self

    def range(self, *args):
        if len(args) == 0:
            return self._range
        if is_iterable(args[0]):
            if len(args[0]) != len(self._domain):
                raise ValueError, 'range specification needs at least two numbers'
            self._range = [
             np.min(args[0]), np.max(args[0])]
        else:
            if len(args) != len(set(args)):
                raise ValueError, 'range values must be unique'
            if list(args) != sorted(list(args)) and list(args)[::-1] != sorted(list(args)):
                raise ValueError, 'range values must be sorted'
            self._range = args
        if len(args) != len(self._domain):
            raise ValueError, 'range specification must have same number of points as domain'
        return self

    def invert(self, y):
        if not self._in_range(x):
            raise ValueError, 'outside range'
        segment = bisect.bisect_right(self._range, y) - 1
        if segment == len(self._range):
            segment -= 1
        return self._inverse((y - self._range[segment]) / (self._range[(segment + 1)] - self._range[segment]) * (self._transform(self._domain[(segment + 1)]) - self._transform(self._domain[segment])) + self._transform(self._domain[segment]))


linear = quantitative

class log(quantitative):
    """Implementation of log scale"""

    def __init__(self, *args):
        self._domain = [
         1, 10]
        quantitative.__init__(self, *args)
        self.base(10)

    def base(self, *args):
        if len(args) == 0:
            return self._base
        else:
            self._base = args[0]
            self._logbase = math.log(self._base)
            self._transform = lambda x: math.log(x) / self._logbase
            self._inverse = lambda y: self._base ** y
            return self


class root(quantitative):
    """root scale"""

    def __init__(self, *args):
        quantitative.__init__(self, *args)
        self.power(2)

    def power(self, *args):
        if len(args) == 0:
            return self._power
        else:
            self._power = args[0]
            self._transform = lambda x: x ** (1.0 / self._power)
            self._inverse = lambda y: y ** self._power
            return self
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/layout/dimension.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 3154 bytes
__doc__ = '\nLayout dimensions are used to give the minimum, maximum and preferred\ndimensions for containers and controls.\n'
from __future__ import unicode_literals
__all__ = ('LayoutDimension', 'sum_layout_dimensions', 'max_layout_dimensions')

class LayoutDimension(object):
    """LayoutDimension"""

    def __init__(self, min=None, max=None, weight=1, preferred=None):
        if not (isinstance(weight, int) and weight > 0):
            raise AssertionError
        else:
            self.min_specified = min is not None
            self.max_specified = max is not None
            self.preferred_specified = preferred is not None
            if min is None:
                min = 0
            if max is None:
                max = 1000000000000000000000000000000
            if preferred is None:
                preferred = min
            self.min = min
            self.max = max
            self.preferred = preferred
            self.weight = weight
            if self.preferred < self.min:
                self.preferred = self.min
            if self.preferred > self.max:
                self.preferred = self.max

    @classmethod
    def exact(cls, amount):
        """
        Return a :class:`.LayoutDimension` with an exact size. (min, max and
        preferred set to ``amount``).
        """
        return cls(min=amount, max=amount, preferred=amount)

    def __repr__(self):
        return 'LayoutDimension(min=%r, max=%r, preferred=%r, weight=%r)' % (
         self.min, self.max, self.preferred, self.weight)

    def __add__(self, other):
        return sum_layout_dimensions([self, other])


def sum_layout_dimensions(dimensions):
    """
    Sum a list of :class:`.LayoutDimension` instances.
    """
    min = sum([d.min for d in dimensions if d.min is not None])
    max = sum([d.max for d in dimensions if d.max is not None])
    preferred = sum([d.preferred for d in dimensions])
    return LayoutDimension(min=min, max=max, preferred=preferred)


def max_layout_dimensions(dimensions):
    """
    Take the maximum of a list of :class:`.LayoutDimension` instances.
    """
    min_ = max([d.min for d in dimensions if d.min is not None])
    max_ = max([d.max for d in dimensions if d.max is not None])
    preferred = max([d.preferred for d in dimensions])
    return LayoutDimension(min=min_, max=max_, preferred=preferred)
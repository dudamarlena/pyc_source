# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/scales/scale_reverse.py
# Compiled at: 2016-07-31 11:30:58
from __future__ import absolute_import, division, print_function, unicode_literals
from .scale import scale
from copy import deepcopy

class scale_y_reverse(scale):
    """
    Reverse y axis

    Examples
    --------
    >>> ggplot(diamonds, aes(x='price')) + geom_histogram() + scale_y_reverse()
    """

    def __radd__(self, gg):
        gg = deepcopy(gg)
        gg.scale_y_reverse = True
        return gg


class scale_x_reverse(scale):
    """
    Reverse x axis

    Examples
    --------
    >>> ggplot(diamonds, aes(x='price')) + geom_histogram() + scale_x_reverse()
    """

    def __radd__(self, gg):
        gg = deepcopy(gg)
        gg.scale_x_reverse = True
        return gg
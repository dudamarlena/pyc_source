# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/scales/scale_y_continuous.py
# Compiled at: 2016-07-11 10:52:39
from __future__ import absolute_import, division, print_function, unicode_literals
from .scale import scale
from copy import deepcopy

class scale_y_continuous(scale):
    """
    Scale y axis as continuous values

    Parameters
    ----------
    breaks: list
        maps to ybreaks
    labels: list
        maps to ytick_labels

    Examples
    --------
    >>> print ggplot(mtcars, aes('mpg', 'qsec')) +     ...     geom_point() +     ...     scale_y_continuous(breaks=[10,20,30],      ...     labels=["horrible", "ok", "awesome"])

    """
    VALID_SCALES = [
     b'name', b'limits', b'labels', b'breaks', b'trans']

    def __radd__(self, gg):
        if self.name:
            gg.ylab = self.name
        if self.limits is not None:
            gg.ylimits = self.limits
        if self.breaks is not None:
            gg.ybreaks = self.breaks
        if self.labels is not None:
            gg.ytick_labels = self.labels
        return gg
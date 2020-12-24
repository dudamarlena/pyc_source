# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/scales/scale_color_yhat.py
# Compiled at: 2016-07-11 10:52:39
from __future__ import absolute_import, division, print_function, unicode_literals
from .scale import scale
from copy import deepcopy

class scale_color_yhat(scale):
    r"""
    Use Yhat's color scheme.

    Examples
    --------
    >>> from ggplot import *
    >>> lng = pd.melt(meat, ['date'])
    >>> gg = ggplot(lng, aes('date', y='beef', color='variable')) + \
    ...     geom_point() + scale_color_yhat()
    """
    VALID_SCALES = []

    def __radd__(self, gg):
        gg.manual_color_list = [
         b'#428bca',
         b'#5cb85c',
         b'#5bc0de',
         b'#f0ad4e',
         b'#d9534f']
        return gg
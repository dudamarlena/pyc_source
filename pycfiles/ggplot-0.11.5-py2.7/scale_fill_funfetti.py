# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/scales/scale_fill_funfetti.py
# Compiled at: 2016-07-31 11:30:58
from __future__ import absolute_import, division, print_function, unicode_literals
from .scale import scale
from copy import deepcopy

class scale_fill_funfetti(scale):
    """
    Make your plots look like funfetti

    Parameters
    ----------
    type: string
        One of confetti or sprinkles (defaults to sprinkles)
        
    Examples
    --------
    >>> from ggplot import *
    >>> p = ggplot(aes(x='carat', fill='clarity'), data=diamonds)
    >>> p += geom_bar()
    >>> print(p + scale_fill_funfetti())
    """
    VALID_SCALES = [
     b'type', b'palette']

    def __radd__(self, gg):
        color_maps = {b'confetti': [
                       b'#a864fd',
                       b'#29cdff',
                       b'#78ff44',
                       b'#ff718d',
                       b'#fdff6a'], 
           b'sprinkles': [
                        b'#F8909F',
                        b'#C5DE9C',
                        b'#8BF3EF',
                        b'#F9AA50',
                        b'#EDE5D9']}
        gg.manual_fill_list = color_maps.get(self.type, color_maps[b'sprinkles'])
        return gg
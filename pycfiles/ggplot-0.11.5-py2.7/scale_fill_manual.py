# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/scales/scale_fill_manual.py
# Compiled at: 2016-07-31 11:30:58
from __future__ import absolute_import, division, print_function, unicode_literals
from .scale import scale
from copy import deepcopy

class scale_fill_manual(scale):
    r"""
    Specify a list of colors to use manually.

    Parameters
    ----------
    values: list of colors/strings
        List of colors with length greater than or equal to the number
        of unique discrete items to which you want to apply color.

    Examples
    --------
    >>> from ggplot import *
    >>> color_list = ['#FFAAAA', '#ff5b00', '#c760ff', '#f43605', '#00FF00',
    ...               '#0000FF', '#4c9085']
    >>> lng = pd.melt(meat, ['date'])
    >>> gg = ggplot(lng, aes('date', fill='variable')) + \
    ...     geom_bar()
    >>> print(gg + scale_fill_manual(values=color_list) + \
    ...     ggtitle('With manual colors'))
    >>> print(gg + ggtitle('Without manual colors'))
    """
    VALID_SCALES = [
     b'values']

    def __radd__(self, gg):
        if self.values is not None:
            n_colors_needed = gg.data[gg._aes.data[b'fill']].nunique()
            n_colors_provided = len(self.values)
            if n_colors_provided < n_colors_needed:
                msg = b'Error: Insufficient values in manual scale. {0} needed but only {1} provided.'
                raise Exception(msg.format(n_colors_needed, n_colors_provided))
            gg.manual_fill_list = self.values[:n_colors_needed]
        return gg
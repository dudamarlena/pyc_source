# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/scales/scale_x_date.py
# Compiled at: 2016-07-11 10:52:39
from __future__ import absolute_import, division, print_function, unicode_literals
from .date_utils import date_breaks, date_format
from .scale import scale
from copy import deepcopy
import six

class scale_x_date(scale):
    r"""
    Position scale, date

    Parameters
    ----------
    labels: 'string / data_format'
        format for your dates
    breaks : string / list of breaks
        1) a string specifying the width between breaks.
        2) the result of a valid call to `date_breaks`
        3) a vector of breaks (TODO: not implemented yet!)

    Examples
    --------
    >>> # 1) manually pass in breaks=date_breaks()
    >>> print(ggplot(meat, aes('date','beef')) + \
    ...       geom_line() + \
    ...       scale_x_date(breaks=date_breaks('10 years'),
    ...           labels=date_format('%B %-d, %Y')))
    >>> # 2) or breaks as just a string
    >>> print(ggplot(meat, aes('date','beef')) + \
    ...       geom_line() + \
    ...       scale_x_date(breaks='10 years',
    ...           labels=date_format('%B %-d, %Y')))
    """
    VALID_SCALES = [
     b'name', b'labels', b'limits', b'breaks', b'trans']

    def __radd__(self, gg):
        gg = deepcopy(gg)
        if self.name:
            gg.xlab = self.name.title()
        if self.labels is not None:
            if isinstance(self.labels, six.string_types):
                self.labels = date_format(self.labels)
            gg.xtick_formatter = self.labels
        if self.limits is not None:
            gg.xlimits = self.limits
        if self.breaks is not None:
            if isinstance(self.breaks, six.string_types):
                self.breaks = date_breaks(self.breaks)
            gg.xmajor_locator = self.breaks
        return gg
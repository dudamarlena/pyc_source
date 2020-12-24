# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/scales/scale_identity.py
# Compiled at: 2016-07-31 11:30:58
from __future__ import absolute_import, division, print_function, unicode_literals
from copy import deepcopy

class scale_identity(object):
    """
    Use the value that you've passed for an aesthetic in the plot without mapping
    it to something else. Classic example is if you have a data frame with a column
    that's like this:
          mycolor
        0    blue
        1     red
        2   green
        3    blue
        4     red
        5    blue
    And you want the actual points you plot to show up as blue, red, or green. Under
    normal circumstances, ggplot will generate a palette for these colors because it
    thinks they are just normal categorical variables. Using scale_identity will make
    it so ggplot uses the values of the field as the aesthetic mapping, so the points
    will show up as the colors you want.
    """
    VALID_SCALES = [
     b'identity_type']

    def __radd__(self, gg):
        gg = deepcopy(gg)
        gg.scale_identity.add(self.identity_type)
        return gg


class scale_alpha_identity(scale_identity):
    """
    See scale_identity
    """
    identity_type = b'alpha'


class scale_color_identity(scale_identity):
    """
    See scale_identity
    """
    identity_type = b'color'


class scale_fill_identity(scale_identity):
    """
    See scale_identity
    """
    identity_type = b'fill'


class scale_linetype_identity(scale_identity):
    """
    See scale_identity
    """
    identity_type = b'linetype'


class scale_shape_identity(scale_identity):
    """
    See scale_identity
    """
    identity_type = b'shape'


class scale_size_identity(scale_identity):
    """
    See scale_identity
    """
    identity_type = b'size'
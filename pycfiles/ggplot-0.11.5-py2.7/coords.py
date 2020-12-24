# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/coords/coords.py
# Compiled at: 2016-07-31 11:30:58
from __future__ import absolute_import, division, print_function, unicode_literals

class coord_polar(object):
    """
    Use polar coordinates for plot
    """

    def __radd__(sefl, gg):
        gg.coords = b'polar'
        return gg


class coord_equal(object):
    """
    Make x and y axes have equal scales
    """

    def __radd__(sefl, gg):
        gg.coords = b'equal'
        return gg


class coord_flip(object):
    """
    Swap x and y coordinates
    """

    def __radd__(sefl, gg):
        gg.coords = b'flip'
        return gg


class coord_cartesian(object):
    """
    Use cartesian coordinate system (this is default)
    """

    def __radd__(sefl, gg):
        gg.coords = b'cartesian'
        return gg
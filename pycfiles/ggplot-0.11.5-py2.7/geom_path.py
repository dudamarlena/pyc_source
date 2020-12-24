# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/geoms/geom_path.py
# Compiled at: 2016-07-31 11:30:58
from .geom_line import geom_line

class geom_path(geom_line):
    """
    Sequence of connected (x, y) coordinates

    Parameters
    ----------
    x:
        x values for (x, y) coordinates
    y:
        y values for (x, y) coordinates
    color:
        color of line
    alpha:
        transparency of color
    linetype:
        type of the line ('solid', 'dashed', 'dashdot', 'dotted')
    size:
        thickness of line

    Examples
    --------
    """
    is_path = True
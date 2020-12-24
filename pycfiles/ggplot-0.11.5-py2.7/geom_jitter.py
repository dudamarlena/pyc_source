# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/geoms/geom_jitter.py
# Compiled at: 2016-07-31 11:30:58
from .geom_point import geom_point

class geom_jitter(geom_point):
    """
    Same as geom_point but with randomness added so you can see the points better

    Parameters
    ----------
    x:
        x values for (x, y) coordinates
    y:
        y values for (x, y) coordinates
    color:
        color of points
    alpha:
        transparency of color
    shape:
        type of point used ('o', '^', 'D', 'v', 's', '*', 'p', '8', "_", "|", "_")
    edgecolors:
        color of the outer line of the point
    size:
        size of the point

    Examples
    --------
    """

    def __init__(self, *args, **kwargs):
        super(geom_point, self).__init__(*args, **kwargs)
        self.params['position'] = 'jitter'
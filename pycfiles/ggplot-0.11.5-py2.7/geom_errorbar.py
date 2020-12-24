# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/geoms/geom_errorbar.py
# Compiled at: 2016-07-31 11:30:58
from .geom_boxplot import geom_boxplot
import matplotlib.pyplot as plt, matplotlib.patches as patches, numpy as np

class geom_errorbar(geom_boxplot):
    """
    Error bar plot

    Parameters
    ----------
    x:
        x values for (x, y) coordinates
    y:
        value to calculate error ranges for
    color:
        color of line
    flier_marker:
        type of marker used ('o', '^', 'D', 'v', 's', '*', 'p', '8', "_", "|", "_")

    Examples
    --------
    """
    DEFAULT_PARAMS = {'outliers': False, 
       'lines': True, 
       'notch': True, 
       'median': False, 
       'box': False}
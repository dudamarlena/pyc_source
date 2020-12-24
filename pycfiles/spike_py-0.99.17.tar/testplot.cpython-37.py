# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Display/testplot.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 830 bytes
"""
testplot

allow to import either matplotlib.pyplor or fakeplot depending on the PLOT flag

usage:

import Display.testplot as testplot
testplot.PLOT = False    # eventually
plt = testplot.plot()

Created by Marc-André on 2012-10-03.
Copyright (c) 2012 IGBMC. All rights reserved.
"""
from __future__ import print_function
import sys
PLOT = True

def plot():
    """
    import the current plotpackage
    usage:

    import spike.Display.testplot as testplot
    plt = testplot.plot()
    
    then use plt as matplotlib
    """
    __import__(plotname())
    return sys.modules[plotname()]


def plotname():
    """returns current plot package name"""
    if PLOT:
        return 'matplotlib.pyplot'
    return 'spike.Display.fakeplot'
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonathanfriedman/Dropbox/python_dev_library/PySurvey/pysurvey/plotting/interactive/PlotClicker.py
# Compiled at: 2013-04-04 09:40:32
"""
Created on Jul 12, 2011

@author: jonathanfriedman
"""
import pylab
from numpy import abs, Inf, asarray

class PlotClicker(object):
    """
    Base class for interacting with plots.
    On mouse click event, get the closest data point to the click, and,
    if within tolerance, perform the action prescribed in the _act method.
    Be sure to indicate what proper format of 'annotes' should be when inheriting.
    """

    def __init__(self, xdata, ydata, **kwargs):
        xdata = asarray(xdata)
        ydata = asarray(ydata)
        self.data = zip(xdata, ydata)
        self.xtol = kwargs.get('xtol', (xdata.max() - xdata.min()) / float(len(xdata)) / 2)
        self.ytol = kwargs.get('ytol', (ydata.max() - ydata.min()) / float(len(ydata)) / 2)
        self.axis = kwargs.get('axis', pylab.gca())
        self.kwargs = kwargs
        pylab.connect('button_press_event', self)

    def _closest2event(self, clickX, clickY, axis='both'):
        """ Get the index and data point that's closest to the mouse event."""
        d_min = Inf
        closest = ()
        for (i, data) in enumerate(self.data):
            (x, y) = data
            dx = abs(clickX - x)
            dy = abs(clickY - y)
            if axis in ('x', 0):
                d = dx
            elif axis in ('y', 1):
                d = dy
            else:
                d = dx + dy
            if d < d_min:
                d_min = d
                closest = (i, x, y, d)

        return closest

    def __call__(self, event):
        if event.inaxes and (self.axis is None or self.axis == event.inaxes):
            clickX = event.xdata
            clickY = event.ydata
            self._act(clickX, clickY)
        return

    def _act(self, clickX, clickY):
        """ Do something with the closest point.
        This method should be overwritten when inheriting.
        """
        closest = self._closest2event(clickX, clickY)
        (i, x, y, d) = closest
        if abs(x - clickX) < self.xtol and abs(y - clickY) < self.ytol:
            pass
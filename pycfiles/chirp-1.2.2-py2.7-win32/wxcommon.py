# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chirp\gui\wxcommon.py
# Compiled at: 2013-12-11 23:17:46
"""
various wxpython-related tools

Copyright (C) 2009 Daniel Meliza <dan // meliza.org>
Created 2009-07-08
"""
import wx, matplotlib
matplotlib.use('WXAgg')
mpl_params = {'axes.hold': False, 'axes.linewidth': 0.5, 
   'ytick.labelsize': 'small', 
   'ytick.direction': 'out', 
   'xtick.labelsize': 'small', 
   'xtick.direction': 'out', 
   'image.aspect': 'auto', 
   'image.origin': 'lower'}
matplotlib.rcParams.update(mpl_params)
from matplotlib.backend_bases import MouseEvent
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from collections import deque

class defaultstack(deque):

    def __init__(self, *args, **kwargs):
        super(defaultstack, self).__init__(*args)
        self.default = kwargs.get('default', None)
        return

    def pop(self):
        if self:
            return super(defaultstack, self).pop()
        return self.default

    def peek(self):
        if self:
            return super(defaultstack, self).__getitem__(-1)
        return self.default


class FigCanvas(FigureCanvasWxAgg):
    """Define a basic figure canvas with a single axes. Contains some basic
    functionality and a few monkey patches to catch some event types unsupported
    in matplotlib.

    """

    def __init__(self, parent, id, figure=None, size=(7.0, 3.0), dpi=100):
        if figure is None:
            figure = Figure(size, dpi)
        super(FigCanvas, self).__init__(parent, id, figure)
        self.figure.set_edgecolor('black')
        self.figure.set_facecolor('white')
        self.SetBackgroundColour(wx.WHITE)
        self.axes = self.figure.add_axes((0.05, 0.1, 0.92, 0.85))
        self.Bind(wx.EVT_MIDDLE_DOWN, self._onMiddleButtonDown)
        self.Bind(wx.EVT_MIDDLE_DCLICK, self._onMiddleButtonDown)
        self.Bind(wx.EVT_MIDDLE_UP, self._onMiddleButtonUp)
        self.mpl_connect('figure_enter_event', self.figure_enter_event)
        self.painter = None
        return

    def _xypos(self, evt):
        return (
         evt.GetX(), evt.GetY())

    def _inaxes(self, x, y):
        evt = MouseEvent('', self, x, self.figure.bbox.height - y)
        return self.axes.in_axes(evt)

    def transform_data(self, point):
        """ Convert canvas location to data location """
        x, y = point
        y = self.figure.bbox.height - y
        return self.axes.transData.inverted().transform_point((x, y))

    def transform_canvas(self, point):
        """ Convert data location to canvas location """
        x, y = self.axes.transData.transform_point(point)
        return (x, self.figure.bbox.height - y)

    def figure_enter_event(self, event):
        self.SetFocus()

    def _onMiddleButtonDown(self, evt):
        """Start measuring on an axis."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        self.CaptureMouse()
        super(FigCanvas, self).button_press_event(x, y, 2, guiEvent=evt)

    def _onMiddleButtonUp(self, evt):
        """End measuring on an axis."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        if self.HasCapture():
            self.ReleaseMouse()
        super(FigCanvas, self).button_release_event(x, y, 2, guiEvent=evt)

    def _onPaint(self, evt):
        self.insideOnPaint = True
        super(FigCanvas, self)._onPaint(evt)
        self.insideOnPaint = False
        dc = wx.PaintDC(self)
        if self.painter is not None:
            self.painter.draw(dc)
        return

    def getDC(self):
        """ Return a client DC for drawing on the figure """
        return wx.ClientDC(self)

    def set_painter(self, painter=None):
        """ Set an active painter. Clears any currently active painter. """
        if self.painter is not None:
            self.painter.reset()
        self.painter = painter
        self.draw()
        return


class Painter(object):
    """Painters encapsulate the mechanics of drawing values in a canvas. Subclasses
     must implement drawValue(), which is called whenever the object needs to be
     repainted, and clearValue(), which is called when the painter is cleared.
     Default implementation stores current and previous values, and erases the
     previous value whenever a new value is supplied.

    @cvar PEN: C{wx.Pen} to use (defaults to C{wx.BLACK_PEN})
    @cvar BRUSH: C{wx.Brush} to use (defaults to C{wx.TRANSPARENT_BRUSH})
    @cvar FUNCTION: Logical function to use (defaults to C{wx.COPY})
    @cvar FONT: C{wx.Font} to use (defaults to C{wx.NORMAL_FONT})
    @cvar TEXT_FOREGROUND: C{wx.Colour} to use (defaults to C{wx.BLACK})
    @cvar TEXT_BACKGROUND: C{wx.Colour} to use (defaults to C{wx.WHITE})

    """
    PEN = wx.BLACK_PEN
    BRUSH = wx.TRANSPARENT_BRUSH
    FUNCTION = wx.COPY
    FONT = wx.NORMAL_FONT
    TEXT_FOREGROUND = wx.BLACK
    TEXT_BACKGROUND = wx.WHITE

    def __init__(self, view):
        self.view = view
        self.lastValue = None
        self.value = None
        return

    def set(self, value):
        self.lastValue = self.value
        self.value = value
        self.draw()

    def reset(self):
        """Reset the stored values of the painter"""
        self.lastValue = self.value = None
        return

    def draw(self, dc=None):
        print dc
        if dc is None:
            dc = wx.BufferedDC(self.view)
        dc.SetPen(self.PEN)
        dc.SetBrush(self.BRUSH)
        dc.SetFont(self.FONT)
        dc.SetTextForeground(self.TEXT_FOREGROUND)
        dc.SetTextBackground(self.TEXT_BACKGROUND)
        dc.SetLogicalFunction(self.FUNCTION)
        dc.BeginDrawing()
        print self.lastValue, self.value
        if self.lastValue is not None:
            self.clearValue(dc, self.lastValue)
            self.lastValue = None
        if self.value is not None:
            self.drawValue(dc, self.value)
        dc.EndDrawing()
        return

    def drawValue(self, dc, value):
        pass

    def clearValue(self, dc, value):
        pass


def addCheckableMenuItems(menu, items):
    """ Add a checkable menu entry to menu for each item in items. This
        method returns a dictionary that maps the menuIds to the
        items. """
    idToItemMapping = {}
    for item in items:
        menuId = wx.NewId()
        idToItemMapping[menuId] = item
        menu.Append(menuId, str(item), kind=wx.ITEM_CHECK)

    return idToItemMapping
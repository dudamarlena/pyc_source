# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mplotlab\graphics\Navigation.py
# Compiled at: 2016-02-07 09:44:32
from mplotlab import App
from matplotlib.backend_bases import NavigationToolbar2
import wx

class Cursors:
    HAND, POINTER, SELECT_REGION, MOVE = list(range(4))


cursors = Cursors()
cursord = {cursors.MOVE: wx.CURSOR_HAND, 
   cursors.HAND: wx.CURSOR_HAND, 
   cursors.POINTER: wx.CURSOR_ARROW, 
   cursors.SELECT_REGION: wx.CURSOR_CROSS}

class Navigation(NavigationToolbar2):

    def __init__(self, *a, **k):
        NavigationToolbar2.__init__(self, *a, **k)

    def _init_toolbar(self, *args, **kwargs):
        pass

    def set_message(self, s):
        """ display in the status bar
        the mouseover data (x,y) 
        """
        try:
            App().mainWin.GetStatusBar().SetStatusText(s, 0)
        except:
            pass

    def set_cursor(self, cursor):
        cursor = wx.StockCursor(cursord[cursor])
        self.canvas.SetCursor(cursor)

    def dynamic_update(self):
        d = self._idle
        self._idle = False
        if d:
            self.canvas.draw()
            self._idle = True

    def press(self, event):
        if self._active == 'ZOOM':
            self.wxoverlay = wx.Overlay()

    def release(self, event):
        if self._active == 'ZOOM':
            self.wxoverlay.Reset()
            del self.wxoverlay

    def draw_rubberband(self, event, x0, y0, x1, y1):
        dc = wx.ClientDC(self.canvas)
        odc = wx.DCOverlay(self.wxoverlay, dc)
        odc.Clear()
        if 'wxMac' not in wx.PlatformInfo:
            dc = wx.GCDC(dc)
        height = self.canvas.figure.bbox.height
        y1 = height - y1
        y0 = height - y0
        if y1 < y0:
            y0, y1 = y1, y0
        if x1 < y0:
            x0, x1 = x1, x0
        w = x1 - x0
        h = y1 - y0
        rect = wx.Rect(x0, y0, w, h)
        rubberBandColor = '#C0C0FF'
        color = wx.NamedColour(rubberBandColor)
        dc.SetPen(wx.Pen(color, 1))
        r, g, b = color.Get()
        color.Set(r, g, b, 96)
        dc.SetBrush(wx.Brush(color))
        dc.DrawRectangleRect(rect)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mplotlab\graphics\GraphicPanel.py
# Compiled at: 2016-02-07 12:04:53
import matplotlib
matplotlib.use('WXAgg')
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as CanvasPanel
from matplotlib.figure import Figure
from GraphicCtlr import GraphicCtlr
from mplotlab.mpl_builders.mpl_figures import buildFigure

class GraphicPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.__figure = Figure()
        self.__canvas = CanvasPanel(self, -1, self.__figure)
        self.__slide = None
        self.__graphicCtrl = GraphicCtlr(self.__canvas)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.__canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(sizer)
        self.Fit()
        self.Show()
        return

    def draw(self):
        self.__canvas.draw()

    def OnPaint(self, event):
        self.draw()

    def getCanvas(self):
        return self.__canvas

    def getFigure(self):
        return self.__figure

    def getGraphicCtrl(self):
        return self.__graphicCtrl

    def getSlide(self):
        return self.__slide

    def setSlide(self, slide):
        self.__slide = slide

    def build(self, *args, **kwargs):
        self.__figure.clear()
        if self.__slide is not None:
            buildFigure(self.__figure, self.__slide)
        return

    def control(self):
        self.__graphicCtrl.control()
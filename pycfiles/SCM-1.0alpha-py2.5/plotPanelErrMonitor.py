# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/plotPanelErrMonitor.py
# Compiled at: 2009-05-29 13:49:21
import wx
from wx import xrc
import sys
from plotPkgErrMonitor import PlotPkgErrMonitor

class PlotPanelErrMonitor(wx.Panel):

    def __init__(self, plotnotebook):
        wx.Panel.__init__(self, plotnotebook.notebook, -1, size=wx.Size(700, 700))
        self.plotnotebook = plotnotebook
        self.paneChildren = {}
        self.paneChildren['errmonitor'] = PlotPkgErrMonitor(self, plotinfo=plotnotebook.plotinfos['errmonitor'], title='', xaxis='Iteration', yaxis='MSE')
        self.paneChildren['errmonitor'].SetEnableGrid(True)
        self.paneChildren['errmonitor'].SetGridColour(wx.ColorRGB(11184810))
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.SetSize(wx.Size(700, 700))

    def OnSize(self, event):
        size = self.GetSize()
        self.paneChildren['errmonitor'].GetPanel().SetPosition(wx.Point(0, 0))
        self.paneChildren['errmonitor'].GetPanel().SetSize(size)
        self.paneChildren['errmonitor'].GetPanel().Update()
        self.Update()

    def updatePlot(self, plotname=''):
        if plotname == '':
            self.updatePlot('errmonitor')
            return
        if self.paneChildren.has_key(plotname) is False:
            return
        plotpkg = self.paneChildren[plotname]
        plotpkg.Update()

    def clear(self):
        pass

    def SetEnableTitle(self, plotname, value):
        if plotname == '':
            self.updatePlot('errmonitor')
            return
        if self.paneChildren.has_key(plotname) is False:
            return
        self.paneChildren[plotname].SetEnableTitle(value)

    def SetTitle(self, plotname, title):
        if plotname == '':
            self.updatePlot('errmonitor')
            return
        if self.paneChildren.has_key(plotname) is False:
            return
        self.paneChildren[plotname].SetTitle(title)

    def ToggleBorderRaised(self, plotname):
        if plotname == '':
            self.updatePlot('errmonitor')
            return
        if self.paneChildren.has_key(plotname) is False:
            return
        self.paneChildren[plotname].ToggleBorderRaised()


if __name__ == '__main__':
    app = wx.PySimpleApp()
    wx.InitAllImageHandlers()
    frame = wx.Frame(None, -1, 'dynamic test', size=(800, 900))
    panel = PlotMainPanel(frame)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()
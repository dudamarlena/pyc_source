# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/plotPanelMacro.py
# Compiled at: 2009-05-29 13:49:10
import wx
from wx import xrc
import sys
from plotPkg import PlotPkg

class PlotPanelMacro(wx.Panel):

    def __init__(self, plotnotebook):
        wx.Panel.__init__(self, plotnotebook.notebook, -1, size=wx.Size(700, 700))
        self.plotnotebook = plotnotebook
        self.paneChildren = {}
        self.paneChildren['macro'] = PlotPkg(self, plotinfo=plotnotebook.plotinfos['macro'], title='', xaxis='Composite or Phase Total Strain (%)', yaxis='Applied or Phase Total Stress (MPa)', xrange=None)
        self.paneChildren['macro'].SetEnableGrid(True)
        self.paneChildren['macro'].SetGridColour(wx.ColorRGB(11184810))
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.SetSize(wx.Size(700, 700))
        return

    def OnSize(self, event):
        size = self.GetSize()
        self.paneChildren['macro'].GetPanel().SetPosition(wx.Point(0, 0))
        self.paneChildren['macro'].GetPanel().SetSize(size)
        self.paneChildren['macro'].GetPanel().Update()
        self.Update()

    def updatePlot(self, plotname=''):
        if plotname == '':
            self.updatePlot('macro')
            return
        if self.paneChildren.has_key(plotname) is False:
            return
        plotpkg = self.paneChildren[plotname]
        plotpkg.Update()

    def clear(self):
        pass

    def SetEnableTitle(self, plotname, value):
        if plotname == '':
            self.updatePlot('macro')
            return
        if self.paneChildren.has_key(plotname) is False:
            return
        self.paneChildren[plotname].SetEnableTitle(value)

    def SetTitle(self, plotname, title):
        if plotname == '':
            self.updatePlot('macro')
            return
        if self.paneChildren.has_key(plotname) is False:
            return
        self.paneChildren[plotname].SetTitle(title)

    def ToggleBorderRaised(self, plotname):
        if plotname == '':
            self.updatePlot('macro')
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
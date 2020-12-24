# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/plotPanelOverview.py
# Compiled at: 2009-05-29 13:49:10
import wx
from wx import xrc
import sys
from plotPkg import PlotPkg
from plotPkgErrMonitor import PlotPkgErrMonitor
from plotPanelSimulation import PlotPanelSimulation

class PlotPanelOverview(wx.Panel):

    def __init__(self, plotnotebook):
        wx.Panel.__init__(self, plotnotebook.notebook, -1, size=wx.Size(700, 700))
        self.plotnotebook = plotnotebook
        self.flagRun = True
        self.paneChildren = {}
        self.paneChildren['macro'] = PlotPkg(self, plotinfo=plotnotebook.plotinfos['macro'], title='Macro', xaxis='Strain (%)', yaxis='Stress (MPa)', xrange=None)
        self.paneChildren['HKL-Long'] = PlotPkg(self, plotinfo=plotnotebook.plotinfos['HKL-Long'], title='HKL-Long', xaxis='Strain (%)', yaxis='Stress (MPa)', xrange=None)
        self.paneChildren['HKL-Trans'] = PlotPkg(self, plotinfo=plotnotebook.plotinfos['HKL-Trans'], title='HKL-Trans', xaxis='Strain (%)', yaxis='Stress (MPa)', xrange=None)
        self.paneChildren['errmonitor'] = PlotPkgErrMonitor(self, plotinfo=plotnotebook.plotinfos['errmonitor'], title='', xaxis='Iteration', yaxis='MSE')
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.SetSize(wx.Size(700, 800))
        return

    def OnSize(self, event):
        gap = 5
        size = self.GetSize()
        size -= wx.Size(gap, gap)
        size.Scale(0.5, 0.5)
        self.paneChildren['HKL-Long'].GetPanel().SetPosition(wx.Point(0, 0))
        self.paneChildren['HKL-Long'].GetPanel().SetSize(size)
        self.paneChildren['HKL-Long'].GetPanel().Update()
        self.paneChildren['HKL-Trans'].GetPanel().SetPosition(wx.Point(size.width + gap, 0))
        self.paneChildren['HKL-Trans'].GetPanel().SetSize(size)
        self.paneChildren['HKL-Trans'].GetPanel().Update()
        self.paneChildren['macro'].GetPanel().SetPosition(wx.Point(0, size.height + gap))
        self.paneChildren['macro'].GetPanel().SetSize(size)
        self.paneChildren['macro'].GetPanel().Update()
        self.paneChildren['errmonitor'].GetPanel().SetPosition(wx.Point(size.width + gap, size.height + gap))
        self.paneChildren['errmonitor'].GetPanel().SetSize(size)
        self.paneChildren['errmonitor'].GetPanel().Update()
        self.Update()

    def updatePlot(self, plotname=''):
        if plotname == '':
            self.updatePlot('HKL-Long')
            self.updatePlot('HKL-Trans')
            self.updatePlot('macro')
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
            self.updatePlot('HKL-Long')
            self.updatePlot('HKL-Trans')
            self.updatePlot('macro')
            self.updatePlot('errmonitor')
            return
        if self.paneChildren.has_key(plotname) is False:
            return
        self.paneChildren[plotname].SetEnableTitle(value)

    def SetTitle(self, plotname, title):
        if plotname == '':
            self.updatePlot('HKL-Long')
            self.updatePlot('HKL-Trans')
            self.updatePlot('macro')
            self.updatePlot('errmonitor')
            return
        if self.paneChildren.has_key(plotname) is False:
            return
        self.paneChildren[plotname].SetTitle(title)

    def ToggleBorderRaised(self, plotname):
        if plotname == '':
            self.updatePlot('HKL-Long')
            self.updatePlot('HKL-Trans')
            self.updatePlot('macro')
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
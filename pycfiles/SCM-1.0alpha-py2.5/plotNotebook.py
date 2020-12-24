# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/plotNotebook.py
# Compiled at: 2009-05-29 13:49:24
import wx
from SCMPanel import SCMPanel
import plotPanelOverview, plotPanelMacro, plotPanelPhase1, plotPanelErrMonitor, plotPanelSimulation

class PlotNotebook(wx.Panel, SCMPanel):

    def __init__(self, *args, **kwds):
        SCMPanel.__init__(self, *args, **kwds)
        wx.Panel.__init__(self, *args, **kwds)
        self.notebook = wx.Notebook(self, -1, style=0)
        self.plotinfos = {}
        self.plotinfos['HKL-Long'] = {}
        self.plotinfos['HKL-Trans'] = {}
        self.plotinfos['macro'] = {}
        self.plotinfos['macro']['model'] = {'name': 'model', 'x': [], 'y': [], 'type': 'line', 'color': 'red', 'width': 1}
        self.plotinfos['macro']['exp'] = {'name': 'exp', 'x': [], 'y': [], 'type': 'marker', 'color': 'blue', 'width': 1}
        self.plotinfos['errmonitor'] = {}
        self.plotinfos['errmonitor']['MSE'] = {'name': 'MSE', 'x': [0], 'y': [0], 'type': 'line', 'color': 'red', 'width': 1}
        self.panes = {}
        self.panes['overview'] = plotPanelOverview.PlotPanelOverview(self)
        self.panes['HKL-Long'] = plotPanelPhase1.PlotPanelPhase1(self, 'HKL-Long')
        self.panes['HKL-Trans'] = plotPanelPhase1.PlotPanelPhase1(self, 'HKL-Trans')
        self.panes['macro'] = plotPanelMacro.PlotPanelMacro(self)
        self.panes['errmonitor'] = plotPanelErrMonitor.PlotPanelErrMonitor(self)
        self.__set_properties()
        self.__do_layout()
        self.panes['overview'].updatePlot()

    def setProperties(self):
        pass

    def __set_properties(self):
        self.notebook.SetMinSize((731, 576))

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.notebook.AddPage(self.panes['overview'], 'Overview')
        self.notebook.AddPage(self.panes['HKL-Long'], 'Phase 1 - HKL-Long')
        self.notebook.AddPage(self.panes['HKL-Trans'], 'Phase 1 - HKL-Trans')
        self.notebook.AddPage(self.panes['macro'], 'Macro')
        self.notebook.AddPage(self.panes['errmonitor'], 'MSE(Mean Square Error)')
        sizer.Add(self.notebook, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        sizer.SetSizeHints(self)

    def updatePlot(self, plotname='', plotinfo={}):
        if self.plotinfos.has_key(plotname):
            self.plotinfos[plotname][plotinfo['name']] = plotinfo
        self.panes['overview'].updatePlot(plotname)
        self.panes['HKL-Long'].updatePlot(plotname)
        self.panes['HKL-Trans'].updatePlot(plotname)
        self.panes['macro'].updatePlot(plotname)
        self.panes['errmonitor'].updatePlot(plotname)

    def clearPlot(self, plotname=''):
        if self.plotinfos.has_key(plotname):
            self.plotinfos[plotname].clear()
        self.panes['overview'].updatePlot(plotname)
        self.panes['HKL-Long'].updatePlot(plotname)
        self.panes['HKL-Trans'].updatePlot(plotname)
        self.panes['macro'].updatePlot(plotname)
        self.panes['errmonitor'].updatePlot(plotname)

    def addError(self, error):
        if not self.plotinfos['errmonitor'].has_key('MSE'):
            self.plotinfos['errmonitor']['MSE'] = {'name': 'MSE', 'x': [0], 'y': [0], 'type': 'line', 'color': 'red', 'width': 1}
        num = len(self.plotinfos['errmonitor']['MSE']['x'])
        self.plotinfos['errmonitor']['MSE']['x'].append(num + 1)
        self.plotinfos['errmonitor']['MSE']['y'].append(error)
        self.panes['overview'].updatePlot('errmonitor')
        self.panes['errmonitor'].updatePlot('errmonitor')

    def clearError(self):
        self.plotinfos['errmonitor']['MSE'] = {'name': 'MSE', 'x': [], 'y': [], 'type': 'line', 'color': 'red', 'width': 1}
        self.panes['overview'].updatePlot('errmonitor')
        self.panes['errmonitor'].updatePlot('errmonitor')

    def SetEnableTitle(self, plotname, value):
        self.panes['overview'].SetEnableTitle(plotname, value)
        self.panes['HKL-Long'].SetEnableTitle(plotname, value)
        self.panes['HKL-Trans'].SetEnableTitle(plotname, value)
        self.panes['macro'].SetEnableTitle(plotname, value)
        self.panes['errmonitor'].SetEnableTitle(plotname, value)

    def SetTitle(self, plotname, title):
        self.panes['overview'].SetTitle(plotname, title)
        self.panes['HKL-Long'].SetTitle(plotname, title)
        self.panes['HKL-Trans'].SetTitle(plotname, title)
        self.panes['macro'].SetTitle(plotname, title)
        self.panes['errmonitor'].SetTitle(plotname, title)

    def ToggleBorderRaised(self, plotname):
        self.panes['overview'].ToggleBorderRaised(plotname)
        self.panes['HKL-Long'].ToggleBorderRaised(plotname)
        self.panes['HKL-Trans'].ToggleBorderRaised(plotname)
        self.panes['macro'].ToggleBorderRaised(plotname)
        self.panes['errmonitor'].ToggleBorderRaised(plotname)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    wx.InitAllImageHandlers()
    frame = wx.Frame(None, -1, 'OPT Panel')
    panel = PlotNotebook(frame)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()
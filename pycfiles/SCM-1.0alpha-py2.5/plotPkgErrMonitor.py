# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/plotPkgErrMonitor.py
# Compiled at: 2009-05-29 13:49:10
import wx
from wx.lib.plot import PlotCanvas
from plotPkg import PlotPkg
import wx.lib.plot as plot

class PlotPkgErrMonitor(PlotPkg):

    def __init__(self, frame, plotinfo, pos=wx.Point(0, 0), size=wx.Size(100, 100), title='', xaxis='Iteration', yaxis='MSE'):
        PlotPkg.__init__(self, frame, plotinfo, pos, size, title, xaxis, yaxis, xrange=None, yrange=None)
        return

    def OnClear(self, evt):
        pass

    def DrawCanvas(self):
        if len(self.plotinfo) == 0:
            PlotPkg.DrawCanvas(self)
            return

        def getFrom(info, name, defaultvalue):
            if info.has_key(name):
                return info[name]
            return defaultvalue

        drawinfos = []
        maxError = 0
        countIter = 10
        for infoname in self.plotinfo:
            info = self.plotinfo[infoname]
            drawdata = self.makePlotData(info['x'], info['y'])
            legend = info['name']
            colour = getFrom(info, 'color', 'black')
            width = getFrom(info, 'width', 1)
            type = getFrom(info, 'type', 'marker')
            if len(drawdata) == 0:
                self.DrawCanvasEmpty()
                return
            if len(drawdata) == 1:
                type = 'marker'
            if type == 'marker':
                drawinfo = plot.PolyMarker(drawdata, legend=legend, colour=colour, width=width)
            elif type == 'line':
                drawinfo = plot.PolyLine(drawdata, legend=legend, colour=colour, width=width)
            drawinfos.append(drawinfo)
            countIter = max(countIter, len(drawdata))
            for (x, y) in drawdata:
                maxError = max(maxError, y)

        gc = plot.PlotGraphics(drawinfos, self.title, self.xaxis, self.yaxis)
        self.canvas.Draw(graphics=gc, xAxis=(0, countIter), yAxis=(0, maxError * 1.2), dc=None)
        return

    def DrawCanvasEmpty(self):
        data = [
         (0, 0)]
        points = plot.PolyLine(data, colour='white', width=0)
        gc = plot.PlotGraphics([points], self.title, self.xaxis, self.yaxis)
        self.canvas.Draw(gc, xAxis=(0, 10), yAxis=(0, 1))


if __name__ == '__main__':
    import Frame
    app = Frame.MyApp(False)
    app.MainLoop()
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/extendedplotframe.py
# Compiled at: 2009-05-29 13:49:17
"""
The module contains Ext
"""
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavToolbar
from matplotlib.figure import Figure
from matplotlib.backends.backend_wx import _load_bitmap
from matplotlib.artist import setp
import wx, os.path
_legendBoxProperties = {'loc': 'upper left', 
   'shadow': True, 
   'numpoints': 3, 
   'pad': 0.2, 
   'labelsep': 0.005, 
   'handlelen': 0.03, 
   'handletextsep': 0.01, 
   'axespad': 0.01}
DATA_SAVE_ID = wx.NewId()

class ExtendedToolbar(NavToolbar):
    """An extended plotting toolbar with a save and close button."""

    def __init__(self, canvas, cankill):
        if wx.Platform != '__WXMAC__':
            NavToolbar.__init__(self, canvas)
        else:
            _realizer = self.Realize

            def f():
                pass

            self.Realize = f
            NavToolbar.__init__(self, canvas)
            self.Realize = _realizer
        self.DeleteToolByPos(6)
        self.DeleteToolByPos(1)
        self.DeleteToolByPos(1)
        self.AddSimpleTool(wx.ID_PRINT, wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_TOOLBAR), 'Print', 'print graph')
        self.AddSeparator()
        self.AddSimpleTool(wx.ID_CLOSE, _load_bitmap('stock_close.xpm'), 'Close window', 'Close window')

    def save(self, evt):
        filetypes = self.canvas._get_imagesave_wildcards()
        exts = []
        sortedtypes = []
        import re
        types = filetypes[0].split('|')
        n = 0
        for ext in types[1::2]:
            res = re.search('\\*\\.(\\w+)', ext)
            pos = n * 2
            if re.search('png', ext):
                pos = 0
            sortedtypes.insert(pos, ext)
            sortedtypes.insert(pos, types[(n * 2)])
            if res:
                exts.insert(pos / 2, res.groups()[0])
            n += 1

        filetypes = ('|').join(sortedtypes)
        dlg = wx.FileDialog(self._parent, 'Save to file', '', '', filetypes, wx.SAVE | wx.OVERWRITE_PROMPT | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetDirectory()
            filename = dlg.GetFilename()
            i = dlg.GetFilterIndex()
            ext = exts[i]
            if '.' not in filename:
                filename = filename + '.' + ext
            self.canvas.print_figure(os.path.join(dirname, filename))


class ExtendedPlotFrame(wx.Frame):
    """An extended plotting frame with a save and close button.

    The class has a matplotlib.figure.Figure data member named 'figure'.
    It also has a matplotlib.axes.Axes data member named 'axes'.
    The normal matplotlib plot manipulations can be performed with these two
    data members. See the matplotlib API at:
    http://matplotlib.sourceforge.net/classdocs.html
    """

    def __init__(self, parent=None, *args, **kwargs):
        """Initialize the CanvasFrame.

        The frame uses ExtendedToolbar as a toolbar, which has a save data
        button and a close button on the toolbar in addition to the normal
        buttons.

        args -- argument list
        kwargs -- keyword argument list
        """
        wx.Frame.__init__(self, parent, -1, 'SCM', size=(550, 350))
        self.figure = Figure(figsize=(0.5, 0.5), dpi=72)
        self.subplot = self.figure.add_subplot(111, autoscale_on=False)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.dirname = ''
        self.filename = ''
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.TOP | wx.LEFT | wx.EXPAND)
        self.toolbar = ExtendedToolbar(self.canvas, True)
        self.toolbar.Realize()
        self.coordLabel = wx.StaticText(self, -1, style=wx.ALIGN_RIGHT | wx.NO_BORDER)
        if wx.Platform == '__WXMAC__':
            self.SetToolBar(self.toolbar)
            self.sizer.Add(self.coordLabel, 0, wx.EXPAND)
        else:
            (tw, th) = self.toolbar.GetSizeTuple()
            (sw, sh) = self.coordLabel.GetSizeTuple()
            (fw, fh) = self.canvas.GetSizeTuple()
            self.coordLabel.SetSize(wx.Size(sw, th))
            barSizer = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer.Add(barSizer, 0, wx.EXPAND | wx.CENTER)
            barSizer.Add(self.toolbar, 0, wx.CENTER)
            barSizer.Add((20, 10), 0)
            barSizer.Add(self.coordLabel, 0, wx.CENTER)
        self.toolbar.update()
        self.SetSizer(self.sizer)
        self.Fit()
        self.SetSize((600, 400))
        self.SetBackgroundColour(self.toolbar.GetBackgroundColour())
        self.canvas.mpl_connect('motion_notify_event', self.UpdateStatusBar)
        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_TOOL(self, DATA_SAVE_ID, self.savePlotData)
        wx.EVT_TOOL(self, wx.ID_CLOSE, self.onClose)
        wx.EVT_CLOSE(self, self.onClose)
        wx.EVT_TOOL(self, wx.ID_PRINT, self.onPrint)
        wx.EVT_TOOL(self, wx.ID_PRINT_SETUP, self.onPrintSetup)
        wx.EVT_TOOL(self, wx.ID_PREVIEW_PRINT, self.onPrintPreview)
        self.datalims = {}

    def onClose(self, evt):
        """Close the frame."""
        if hasattr(self, 'plotter'):
            self.plotter.onWindowClose()
        self.Destroy()

    def OnPaint(self, event):
        self.canvas.draw()
        event.Skip()

    def savePlotData(self, evt):
        """Save the data in the plot in columns."""
        d = wx.FileDialog(None, 'Save as...', self.dirname, self.filename, '(*.dat)|*.dat|(*.txt)|*.txt|(*)|*', wx.SAVE | wx.OVERWRITE_PROMPT)
        if d.ShowModal() == wx.ID_OK:
            fullname = d.GetPath()
            self.dirname = os.path.dirname(fullname)
            self.filename = os.path.basename(fullname)
        d.Destroy()
        return

    def onPrint(self, evt):
        """handle print event"""
        self.canvas.Printer_Print(event=evt)

    def onPrintSetup(self, event=None):
        self.canvas.Printer_Setup(event=event)

    def onPrintPreview(self, event=None):
        self.canvas.Printer_Preview(event=event)

    def UpdateStatusBar(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            xystr = 'x = %g, y = %g' % (x, y)
            self.coordLabel.SetLabel(xystr)

    def replot(self):
        """officially call function in matplotlib to do drawing
        """
        self.canvas.draw()

    def insertCurve(self, xData, yData, style):
        """insert a new curve to the plot

        xData, yData -- x, y data to used for the curve
        style -- the way curve should be plotted
        return:  internal reference to the newly added curve
        """
        (stylestr, properties) = self.__translateStyles(style)
        curveRef = self.subplot.plot(xData, yData, stylestr, **properties)[0]
        self.subplot.legend(**_legendBoxProperties)
        try:
            self.datalims[curveRef] = (
             min(xData), max(xData), min(yData), max(yData))
        except ValueError:
            self.datalims[curveRef] = (0, 0, 0, 0)

        self.__updateViewLimits()
        return curveRef

    def updateData(self, curveRef, xData, yData):
        """update data for a existing curve

        curveRef -- internal reference to a curve
        xData, yData -- x, y data to used for the curve
        """
        curveRef.set_data(xData, yData)
        try:
            self.datalims[curveRef] = (
             min(xData), max(xData), min(yData), max(yData))
        except ValueError:
            self.datalims[curveRef] = (0, 0, 0, 0)

        self.__updateViewLimits()

    def changeStyle(self, curveRef, style):
        """change curve style

        curveRef -- internal reference to curves
        style -- style dictionary
        """
        (stylestr, properties) = self.__translateStyles(style)
        setp((curveRef,), **properties)
        self.subplot.legend(**_legendBoxProperties)

    def removeCurve(self, curveRef):
        """remove curve from plot

        curveRef -- internal reference to curves
        """
        del self.datalims[curveRef]
        self.figure.gca().lines.remove(curveRef)
        self.subplot.legend(**_legendBoxProperties)
        self.__updateViewLimits()

    def __updateViewLimits(self):
        """adjust the subplot range in order to show all curves correctly.
        """
        if len(self.datalims) == 0:
            return
        self.subplot.dataLim.ignore(True)
        bounds = self.datalims.values()
        xmin = min([ b[0] for b in bounds ])
        xmax = max([ b[1] for b in bounds ])
        ymin = min([ b[2] for b in bounds ])
        ymax = max([ b[3] for b in bounds ])
        if xmax > xmin:
            self.subplot.set_xlim(xmin, xmax)
        if ymax > ymin:
            self.subplot.set_ylim(ymin, ymax)

    def __translateStyles(self, style):
        """Private function to translate general probabilities to
        Matplotlib specific ones

        style -- general curve style dictionary ( defined in demoplot )
        """
        lineStyleDict = {'solid': '-', 'dash': '--', 'dot': ':', 'dashDot': '-.'}
        symbolDict = {'diamond': 'd', 'square': 's', 'circle': 'o', 'cross': '+', 
           'xCross': 'x', 'triangle': '^'}
        colorDict = {'blue': 'b', 'green': 'g', 'red': 'r', 'cyan': 'c', 'magenta': 'm', 
           'yellow': 'y', 'black': 'k', 'white': 'w', 'darkRed': '#8B0000', 
           'darkGreen': '#006400', 'darkCyan': '#008B8B', 'darkYellow': '#FFD700', 
           'darkBlue': '#00008B', 'darkMagenta': '#8B008B'}
        properties = {}
        stylestr = ''
        color = colorDict.get(style['color'], 'k')
        if style['with'] in ('points', 'linespoints'):
            stylestr = '.'
            symbol = symbolDict.get(style['symbol'], 's')
            symbolSize = style['symbolSize']
            symbolColor = colorDict.get(style['symbolColor'], 'k')
            properties.update({'markerfacecolor': symbolColor, 
               'markeredgecolor': color, 
               'marker': symbol, 
               'markersize': symbolSize})
        if style['with'] != 'points':
            lineStyle = lineStyleDict.get(style['line'], '-')
            lineWidth = style['width']
            stylestr += lineStyle
            properties.update({'color': color, 'linestyle': lineStyle, 'linewidth': lineWidth})
        if style.has_key('legend'):
            properties['label'] = style['legend']
        return (
         stylestr, properties)

    def setTitle(self, wt, gt):
        """set graph labels

        wt -- window title
        gt -- graph title
        """
        self.SetTitle(wt)
        self.figure.gca().set_title(gt)

    def setXLabel(self, x):
        """set label for x axis

        x -- x label
        """
        self.figure.gca().set_xlabel(x)

    def setYLabel(self, y):
        """set label for y axis

        y -- y label
        """
        self.figure.gca().set_ylabel(y)

    def clear(self):
        """erase all curves"""
        self.subplot.clear()
        self.curverefs = []
        self.replot()


if __name__ == '__main__':

    class MyApp(wx.App):

        def OnInit(self):
            from matplotlib.numerix import arange, sin, pi, cos
            x = arange(0.0, 3.0, 0.01)
            s = sin(2 * pi * x)
            c = cos(2 * pi * x)
            t = sin(2 * pi * x) + cos(2 * pi * x)
            frame = ExtendedPlotFrame(None)
            style = {'with': 'lines', 'color': 'blue', 'line': 'solid', 'width': 2}
            style['legend'] = 'sin(x)'
            frame.insertCurve(x, s, style)
            style['legend'] = 'cos(x)'
            frame.insertCurve(x, c, style)
            style = {'with': 'lines', 'color': 'black', 'line': 'solid', 'width': 2}
            frame.insertCurve(x, t, style)
            frame.Show(True)
            return True


    app = MyApp(0)
    app.MainLoop()
__id__ = '$Id: extendedplotframe.py 1883 2008-02-11 22:35:52Z juhas $'
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/plotexplorer_gui.py
# Compiled at: 2015-02-03 14:48:35
__doc__ = '\nCopyright (c) 2012, Robert Steed\nAll rights reserved.\n\nRedistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:\n\n    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.\n    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.\n\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n'
import wx
from wx.lib.mixins.listctrl import ColumnSorterMixin, CheckListCtrlMixin
import numpy as N
from matplotlib import use as pluse
pluse('WxAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

class plotchooser(wx.ListCtrl, CheckListCtrlMixin, ColumnSorterMixin):
    """the listctrl stores entries with multiple columns. The ColumnSorterMixin allows the entries to be sorted with respect to different columns
    and the checklistctrlMixin adds a check box to each entry. The class will tell you an entries index but since these change with each reordering
    we need to store some data with each entry in order to work out which plot it refers to"""

    def __init__(self, parent, colnum):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        CheckListCtrlMixin.__init__(self)
        ColumnSorterMixin.__init__(self, colnum)
        self.itemDataMap = {}

    def GetListCtrl(self):
        return self

    def GetSecondarySortValues(self, col, key1, key2):
        """Returns a tuple of 2 values to use for secondary sort values when the
           items in the selected column match equal.  The default just returns the
           item data values."""
        item1 = self.itemDataMap[key1]
        item2 = self.itemDataMap[key2]
        items = zip(item1, item2)
        for i1, i2 in items[col + 1:] + items[:col]:
            if i1 != i2:
                return (i1, i2)

        return (key1, key2)

    def OnCheckItem(self, index, flag):
        key = self.GetItemData(index)
        address = self.itemDataMap[key]
        self.GetParent().GetParent().GetParent().plotshow(address, flag)

    def refreshColumns(self, columnhdr):
        self.DeleteAllColumns()
        for hdr in columnhdr:
            self.InsertColumn(1000000.0, hdr, width=80)

    def refreshEntries(self, plotset):
        self.DeleteAllItems()
        for address in plotset:
            index = self.InsertStringItem(1000000.0, 'blaah')
            for i, ad in enumerate(address):
                self.SetStringItem(index, i, str(ad))

            self.SetItemData(index, index)
            self.itemDataMap[index] = address


class DataExplorerGUI(wx.Frame):

    def __init__(self, data, fits, labels, styles, parent, id, title):
        """a gui for exploring data stored in dictionary 'data'. 
        data = a dictionary of x,y arrays to plot where the keys are tuples (of equal length)"""
        wx.Frame.__init__(self, parent, id, title, size=(380, 230))
        strkeys = sum([ 1 for i in data if type(i) in (type(''), type(0), type(float())) ])
        tplkeys = sum([ 1 for i in data if type(i) in (type(()), type([])) ])
        assert min(strkeys, tplkeys) == 0
        if strkeys == len(data):
            tmp = {}
            for key, value in data.items():
                tmp[(key,)] = value

            data = tmp
            del tmp
            self.cols = cols = 1
        elif tplkeys == len(data):
            self.cols = cols = len(data.keys()[0])
            assert len([ False for i in data.keys() if len(i) != cols ]) == 0
        self.data = data
        if fits != None:
            self.fits = fits
        else:
            self.fits = {}
        if labels != None:
            assert len(labels) == 3
            if type(labels[2]) not in (type(()), type([])):
                assert cols == 1
            else:
                assert len(labels[2]) == cols
        else:
            labels = [
             '', '', ['A', 'B', 'C', 'D', 'E', 'F', 'G'][:cols]]
        if styles != None:
            self.styles = styles
        else:
            self.styles = {}
        self.Plots1 = {}
        self.FPlots1 = {}
        self.showlegend = False
        self.legendloc = 'best'
        self.stop_refresh_hack = False
        splitter = wx.SplitterWindow(self, -1)
        leftpanel = wx.Panel(splitter, -1)
        rightpanel = wx.Panel(splitter, -1)
        self.plotchooser = plotchooser(rightpanel, cols)
        self.plotchooser.refreshColumns(labels[2])
        self.plotchooser.refreshEntries(data.keys())
        self.selectall = wx.Button(rightpanel, -1, 'Select All')
        self.Bind(wx.EVT_BUTTON, self.plotall, self.selectall)
        self.selectnone = wx.Button(rightpanel, -1, 'Select None')
        self.Bind(wx.EVT_BUTTON, self.plotnone, self.selectnone)
        self.fig = Figure()
        self.canvas = FigureCanvas(leftpanel, -1, self.fig)
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.set_xlabel(labels[0])
        self.ax1.set_ylabel(labels[1])
        self.fig.subplots_adjust(left=0.1, bottom=0.07, right=0.95, top=0.95)
        self.toolbar = NavigationToolbar2WxAgg(self.canvas)
        self.bresetzoom = wx.Button(leftpanel, -1, 'Reset Zoom')
        self.Bind(wx.EVT_BUTTON, self.resetzoom, self.bresetzoom)
        self.bsavedata = wx.Button(leftpanel, -1, 'Save Data')
        self.Bind(wx.EVT_BUTTON, self.savedata, self.bsavedata)
        self.legendch = wx.CheckBox(leftpanel, -1, 'Show Legend')
        self.Bind(wx.EVT_CHECKBOX, self.evt_legendch, self.legendch)
        self.cursorPos = wx.StaticText(leftpanel, -1, 'x=0.000000 \ny=0.000000  ', style=wx.ALIGN_LEFT)
        self.canvas.mpl_connect('motion_notify_event', self.UpdateStatusBar)
        self.canvas.mpl_connect('key_press_event', self.press)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(self.canvas, 15, wx.EXPAND)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.toolbar, 1, wx.LEFT | wx.EXPAND)
        hbox2.Add(self.bresetzoom, 0, wx.LEFT | wx.TOP | wx.BOTTOM, border=6)
        hbox2.Add(self.bsavedata, 0, wx.ALL, border=6)
        hbox2.Add(self.legendch, 0, wx.ALL, border=6)
        hbox2.Add(self.cursorPos, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT, border=6)
        vbox1.Add(hbox2, 1, wx.EXPAND)
        leftpanel.SetSizer(vbox1)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.plotchooser, 2, wx.EXPAND)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(self.selectall, 0, wx.ALL, border=6)
        hbox3.Add(self.selectnone, 0, wx.ALL, border=6)
        vbox2.Add(hbox3, 0)
        rightpanel.SetSizer(vbox2)
        splitter.SplitVertically(leftpanel, rightpanel, -200)
        splitter.SetMinimumPaneSize(50)
        splitter.SetSashGravity(0.5)
        topsizer = wx.BoxSizer(wx.HORIZONTAL)
        topsizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(topsizer)
        topsizer.Fit(self)
        self.toolbar.update()
        self.Show(True)
        return

    def plotshow(self, address, show, refresh_canvas=True):
        label = (' ').join([ str(j) for j in address ])
        ax, Plots, FPlots = self.ax1, self.Plots1, self.FPlots1
        if show:
            fitfunc = self.fits.get(address, None)
            x, y = self.data[address]
            if type(fitfunc) != type(None):
                style = 'x'
            else:
                style = self.styles.get(address, '-')
            line, = ax.plot(x, y, style, label=label)
            Plots[address] = line
            if type(fitfunc) != type(None):
                xlen = x[(-1)] - x[0]
                x2 = N.linspace(x[0] - 0.25 * xlen, x[(-1)] + 0.25 * xlen, 50)
                y2 = fitfunc(x2)
                cr = line.get_color()
                line2, = ax.plot(x2, y2, '-' + cr, label='_nolegend_')
                FPlots[address] = line2
        else:
            line = Plots[address]
            ax.lines.remove(line)
            del Plots[address]
            if FPlots.has_key(address):
                line = FPlots[address]
                ax.lines.remove(line)
                del FPlots[address]
        ax.relim()
        if self.ax1.lines != [] and self.showlegend:
            self.ax1.legend(loc=self.legendloc)
        else:
            self.ax1.legend_ = None
        if self.stop_refresh_hack != True:
            self.canvas.draw()
        return

    def evt_legendch(self, event):
        ch = event.IsChecked()
        self.showlegend = ch
        if ch and self.ax1.lines != []:
            self.ax1.legend(loc=self.legendloc)
        else:
            self.ax1.legend_ = None
        self.canvas.draw()
        return

    def plotall(self, event):
        pch = self.plotchooser
        self.stop_refresh_hack = True
        for index in range(pch.ItemCount):
            flag = True
            pch.CheckItem(index, flag)

        self.stop_refresh_hack = False
        self.canvas.draw()

    def plotnone(self, event):
        pch = self.plotchooser
        self.stop_refresh_hack = True
        for index in range(pch.ItemCount):
            flag = False
            pch.CheckItem(index, flag)

        self.stop_refresh_hack = False
        self.canvas.draw()

    def resetzoom(self, event):
        self.ax1.autoscale()
        self.canvas.draw()

    def savedata(self, event):
        """saving visible data"""
        wildcard = 'csv file (*.csv)|*.csv|All files (*.*)|*.*'
        delimiter = ','
        dlg = wx.FileDialog(self, message='Save file as ...', defaultFile='', wildcard=wildcard, style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            Plotted = self.Plots1.keys()
            data = self.data
            visdata = sum([ list(data[address]) for address in Plotted ], [])
            lengths = [ len(array) for array in visdata ]
            maxlen = max(lengths)
            visdata = [ N.resize(array, (maxlen,)) for array in visdata ]
            for array, length in zip(visdata, lengths):
                array[length:] = 0.0

            visdata = N.column_stack(visdata)
            colhdr = [ [ str(Plotted[i][j]) for i in range(len(Plotted)) ] for j in range(len(Plotted[0])) ]
            colhdr = [ delimiter.join(sum([ [i, i] for i in line ], [])) + '\n' for line in colhdr ]
            fobj = file(path, 'w')
            fobj.writelines(colhdr)
            N.savetxt(fobj, visdata, delimiter=delimiter, fmt='%.14g')
            fobj.close()
        dlg.Destroy()

    def press(self, event):
        key_press_handler(event, self.canvas, self.toolbar)

    def UpdateStatusBar(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            self.cursorPos.SetLabel('x= %.6g\ny= %.6g' % (x, y))


class DataExplorer(wx.App):

    def __init__(self, datadict, fits=None, labels=None, styles=None, title='plotexplorer', *pargs, **kwargs):
        self.data = datadict
        self.fits = fits
        self.labels = labels
        self.styles = styles
        self.title = title
        wx.App.__init__(self, *pargs, **kwargs)

    def OnInit(self):
        self.frame = DataExplorerGUI(self.data, self.fits, self.labels, self.styles, None, -1, self.title)
        self.frame.Show(True)
        return True


if __name__ == '__main__':
    data1 = {'This': (N.arange(10), N.arange(10) ** 2), 'Is': (N.arange(3, 15, 1), 50 * N.sin(N.arange(3, 15, 1)))}
    data2 = {('This', 'Is'): (N.arange(10), N.arange(10) ** 2), ('Another', 'test'): (N.arange(3, 15, 1), 50 * N.sin(N.arange(3, 15, 1)))}
    labels1 = (
     'work', 'fun', ('mango', ))
    labels2 = ('work', 'fun', ('freq', 'mango'))
    app = DataExplorer(data2, fits=None, labels=labels2, redirect=False)
    app.MainLoop()
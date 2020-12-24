# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/exporters/Matplotlib.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 4821 bytes
from ..Qt import QtGui, QtCore
from .Exporter import Exporter
from .. import PlotItem
from .. import functions as fn
__all__ = ['MatplotlibExporter']

class MatplotlibExporter(Exporter):
    Name = 'Matplotlib Window'
    windows = []

    def __init__(self, item):
        Exporter.__init__(self, item)

    def parameters(self):
        pass

    def cleanAxes(self, axl):
        if type(axl) is not list:
            axl = [
             axl]
        for ax in axl:
            if ax is None:
                continue
            for loc, spine in ax.spines.iteritems():
                if loc in ('left', 'bottom'):
                    pass
                elif loc in ('right', 'top'):
                    spine.set_color('none')
                else:
                    raise ValueError('Unknown spine location: %s' % loc)
                ax.xaxis.set_ticks_position('bottom')

    def export(self, fileName=None):
        if isinstance(self.item, PlotItem):
            mpw = MatplotlibWindow()
            MatplotlibExporter.windows.append(mpw)
            stdFont = 'Arial'
            fig = mpw.getFigure()
            xlabel = self.item.axes['bottom']['item'].label.toPlainText()
            ylabel = self.item.axes['left']['item'].label.toPlainText()
            title = self.item.titleLabel.text
            ax = fig.add_subplot(111, title=title)
            ax.clear()
            self.cleanAxes(ax)
            for item in self.item.curves:
                x, y = item.getData()
                opts = item.opts
                pen = fn.mkPen(opts['pen'])
                if pen.style() == QtCore.Qt.NoPen:
                    linestyle = ''
                else:
                    linestyle = '-'
                color = tuple([c / 255.0 for c in fn.colorTuple(pen.color())])
                symbol = opts['symbol']
                if symbol == 't':
                    symbol = '^'
                symbolPen = fn.mkPen(opts['symbolPen'])
                symbolBrush = fn.mkBrush(opts['symbolBrush'])
                markeredgecolor = tuple([c / 255.0 for c in fn.colorTuple(symbolPen.color())])
                markerfacecolor = tuple([c / 255.0 for c in fn.colorTuple(symbolBrush.color())])
                markersize = opts['symbolSize']
                if opts['fillLevel'] is not None:
                    if opts['fillBrush'] is not None:
                        fillBrush = fn.mkBrush(opts['fillBrush'])
                        fillcolor = tuple([c / 255.0 for c in fn.colorTuple(fillBrush.color())])
                        ax.fill_between(x=x, y1=y, y2=(opts['fillLevel']), facecolor=fillcolor)
                pl = ax.plot(x, y, marker=symbol, color=color, linewidth=(pen.width()), linestyle=linestyle,
                  markeredgecolor=markeredgecolor,
                  markerfacecolor=markerfacecolor,
                  markersize=markersize)
                xr, yr = self.item.viewRange()
                (ax.set_xbound)(*xr)
                (ax.set_ybound)(*yr)

            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            mpw.draw()
        else:
            raise Exception('Matplotlib export currently only works with plot items')


MatplotlibExporter.register()

class MatplotlibWindow(QtGui.QMainWindow):

    def __init__(self):
        from ..widgets import MatplotlibWidget
        QtGui.QMainWindow.__init__(self)
        self.mpl = MatplotlibWidget.MatplotlibWidget()
        self.setCentralWidget(self.mpl)
        self.show()

    def __getattr__(self, attr):
        return getattr(self.mpl, attr)

    def closeEvent(self, ev):
        MatplotlibExporter.windows.remove(self)
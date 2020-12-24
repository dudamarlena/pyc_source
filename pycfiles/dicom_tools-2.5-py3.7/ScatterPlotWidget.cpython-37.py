# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/ScatterPlotWidget.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 8440 bytes
from ..Qt import QtGui, QtCore
from .PlotWidget import PlotWidget
from .DataFilterWidget import DataFilterParameter
from .ColorMapWidget import ColorMapParameter
from .. import parametertree as ptree
from .. import functions as fn
from .. import getConfigOption
import graphicsItems.TextItem as TextItem
import numpy as np
from ..pgcollections import OrderedDict
__all__ = ['ScatterPlotWidget']

class ScatterPlotWidget(QtGui.QSplitter):
    __doc__ = '\n    This is a high-level widget for exploring relationships in tabular data.\n        \n    Given a multi-column record array, the widget displays a scatter plot of a\n    specific subset of the data. Includes controls for selecting the columns to\n    plot, filtering data, and determining symbol color and shape.\n    \n    The widget consists of four components:\n    \n    1) A list of column names from which the user may select 1 or 2 columns\n       to plot. If one column is selected, the data for that column will be\n       plotted in a histogram-like manner by using :func:`pseudoScatter()\n       <pyqtgraph.pseudoScatter>`. If two columns are selected, then the\n       scatter plot will be generated with x determined by the first column\n       that was selected and y by the second.\n    2) A DataFilter that allows the user to select a subset of the data by \n       specifying multiple selection criteria.\n    3) A ColorMap that allows the user to determine how points are colored by\n       specifying multiple criteria.\n    4) A PlotWidget for displaying the data.\n    '

    def __init__(self, parent=None):
        QtGui.QSplitter.__init__(self, QtCore.Qt.Horizontal)
        self.ctrlPanel = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.addWidget(self.ctrlPanel)
        self.fieldList = QtGui.QListWidget()
        self.fieldList.setSelectionMode(self.fieldList.ExtendedSelection)
        self.ptree = ptree.ParameterTree(showHeader=False)
        self.filter = DataFilterParameter()
        self.colorMap = ColorMapParameter()
        self.params = ptree.Parameter.create(name='params', type='group', children=[self.filter, self.colorMap])
        self.ptree.setParameters((self.params), showTop=False)
        self.plot = PlotWidget()
        self.ctrlPanel.addWidget(self.fieldList)
        self.ctrlPanel.addWidget(self.ptree)
        self.addWidget(self.plot)
        bg = fn.mkColor(getConfigOption('background'))
        bg.setAlpha(150)
        self.filterText = TextItem(border=(getConfigOption('foreground')), color=bg)
        self.filterText.setPos(60, 20)
        self.filterText.setParentItem(self.plot.plotItem)
        self.data = None
        self.mouseOverField = None
        self.scatterPlot = None
        self.style = dict(pen=None, symbol='o')
        self.fieldList.itemSelectionChanged.connect(self.fieldSelectionChanged)
        self.filter.sigFilterChanged.connect(self.filterChanged)
        self.colorMap.sigColorMapChanged.connect(self.updatePlot)

    def setFields(self, fields, mouseOverField=None):
        """
        Set the list of field names/units to be processed.
        
        The format of *fields* is the same as used by 
        :func:`ColorMapWidget.setFields <pyqtgraph.widgets.ColorMapWidget.ColorMapParameter.setFields>`
        """
        self.fields = OrderedDict(fields)
        self.mouseOverField = mouseOverField
        self.fieldList.clear()
        for f, opts in fields:
            item = QtGui.QListWidgetItem(f)
            item.opts = opts
            item = self.fieldList.addItem(item)

        self.filter.setFields(fields)
        self.colorMap.setFields(fields)

    def setData(self, data):
        """
        Set the data to be processed and displayed. 
        Argument must be a numpy record array.
        """
        self.data = data
        self.filtered = None
        self.updatePlot()

    def fieldSelectionChanged(self):
        sel = self.fieldList.selectedItems()
        if len(sel) > 2:
            self.fieldList.blockSignals(True)
            try:
                for item in sel[1:-1]:
                    item.setSelected(False)

            finally:
                self.fieldList.blockSignals(False)

        self.updatePlot()

    def filterChanged(self, f):
        self.filtered = None
        self.updatePlot()
        desc = self.filter.describe()
        if len(desc) == 0:
            self.filterText.setVisible(False)
        else:
            self.filterText.setText('\n'.join(desc))
            self.filterText.setVisible(True)

    def updatePlot(self):
        self.plot.clear()
        if self.data is None:
            return
        if self.filtered is None:
            self.filtered = self.filter.filterData(self.data)
        data = self.filtered
        if len(data) == 0:
            return
        colors = np.array([(fn.mkBrush)(*x) for x in self.colorMap.map(data)])
        style = self.style.copy()
        sel = list([str(item.text()) for item in self.fieldList.selectedItems()])
        units = list([item.opts.get('units', '') for item in self.fieldList.selectedItems()])
        if len(sel) == 0:
            self.plot.setTitle('')
            return
        if len(sel) == 1:
            self.plot.setLabels(left=('N', ''), bottom=(sel[0], units[0]), title='')
            if len(data) == 0:
                return
            xy = [data[sel[0]], None]
        else:
            if len(sel) == 2:
                self.plot.setLabels(left=(sel[1], units[1]), bottom=(sel[0], units[0]))
                if len(data) == 0:
                    return
                xy = [
                 data[sel[0]], data[sel[1]]]
            else:
                enum = [
                 False, False]
                for i in (0, 1):
                    axis = self.plot.getAxis(['bottom', 'left'][i])
                    if not xy[i] is not None or self.fields[sel[i]].get('mode', None) == 'enum' or xy[i].dtype.kind in ('S',
                                                                                                                        'O'):
                        vals = self.fields[sel[i]].get('values', list(set(xy[i])))
                        xy[i] = np.array([vals.index(x) if x in vals else len(vals) for x in xy[i]], dtype=float)
                        axis.setTicks([list(enumerate(vals))])
                        enum[i] = True
                    else:
                        axis.setTicks(None)

                mask = np.ones((len(xy[0])), dtype=bool)
                if xy[0].dtype.kind == 'f':
                    mask &= ~np.isnan(xy[0])
                if xy[1] is not None:
                    if xy[1].dtype.kind == 'f':
                        mask &= ~np.isnan(xy[1])
                    xy[0] = xy[0][mask]
                    style['symbolBrush'] = colors[mask]
                    if xy[1] is None:
                        xy[1] = fn.pseudoScatter(xy[0])
                else:
                    xy[1] = xy[1][mask]
                    for ax in (0, 1):
                        if not enum[ax]:
                            continue
                        imax = int(xy[ax].max()) if len(xy[ax]) > 0 else 0
                        for i in range(imax + 1):
                            keymask = xy[ax] == i
                            scatter = fn.pseudoScatter((xy[(1 - ax)][keymask]), bidir=True)
                            if len(scatter) == 0:
                                continue
                            smax = np.abs(scatter).max()
                            if smax != 0:
                                scatter *= 0.2 / smax
                            xy[ax][keymask] += scatter

            if self.scatterPlot is not None:
                try:
                    self.scatterPlot.sigPointsClicked.disconnect(self.plotClicked)
                except:
                    pass

            self.scatterPlot = (self.plot.plot)(xy[0], xy[1], data=data[mask], **style)
            self.scatterPlot.sigPointsClicked.connect(self.plotClicked)

    def plotClicked(self, plot, points):
        pass
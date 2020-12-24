# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/flowchart/library/Display.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 10343 bytes
from ..Node import Node
import weakref
from ...Qt import QtCore, QtGui
import graphicsItems.ScatterPlotItem as ScatterPlotItem
import graphicsItems.PlotCurveItem as PlotCurveItem
from ... import PlotDataItem, ComboBox
from .common import *
import numpy as np

class PlotWidgetNode(Node):
    __doc__ = 'Connection to PlotWidget. Will plot arrays, metaarrays, and display event lists.'
    nodeName = 'PlotWidget'
    sigPlotChanged = QtCore.Signal(object)

    def __init__(self, name):
        Node.__init__(self, name, terminals={'In': {'io':'in',  'multi':True}})
        self.plot = None
        self.plots = {}
        self.ui = None
        self.items = {}

    def disconnected(self, localTerm, remoteTerm):
        if localTerm is self['In']:
            if remoteTerm in self.items:
                self.plot.removeItem(self.items[remoteTerm])
                del self.items[remoteTerm]

    def setPlot(self, plot):
        if plot == self.plot:
            return
        if self.plot is not None:
            for vid in list(self.items.keys()):
                self.plot.removeItem(self.items[vid])
                del self.items[vid]

        self.plot = plot
        self.updateUi()
        self.update()
        self.sigPlotChanged.emit(self)

    def getPlot(self):
        return self.plot

    def process(self, In, display=True):
        if display:
            if self.plot is not None:
                items = set()
                for name, vals in In.items():
                    if vals is None:
                        continue
                    if type(vals) is not list:
                        vals = [
                         vals]
                    for val in vals:
                        vid = id(val)
                        if vid in self.items and self.items[vid].scene() is self.plot.scene():
                            items.add(vid)
                        else:
                            if isinstance(val, QtGui.QGraphicsItem):
                                self.plot.addItem(val)
                                item = val
                            else:
                                item = self.plot.plot(val)
                            self.items[vid] = item
                            items.add(vid)

                for vid in list(self.items.keys()):
                    if vid not in items:
                        self.plot.removeItem(self.items[vid])
                        del self.items[vid]

    def processBypassed(self, args):
        if self.plot is None:
            return
        for item in list(self.items.values()):
            self.plot.removeItem(item)

        self.items = {}

    def ctrlWidget(self):
        if self.ui is None:
            self.ui = ComboBox()
            self.ui.currentIndexChanged.connect(self.plotSelected)
            self.updateUi()
        return self.ui

    def plotSelected(self, index):
        self.setPlot(self.ui.value())

    def setPlotList(self, plots):
        """
        Specify the set of plots (PlotWidget or PlotItem) that the user may
        select from.
        
        *plots* must be a dictionary of {name: plot} pairs.
        """
        self.plots = plots
        self.updateUi()

    def updateUi(self):
        self.ui.setItems(self.plots)
        try:
            self.ui.setValue(self.plot)
        except ValueError:
            pass


class CanvasNode(Node):
    __doc__ = 'Connection to a Canvas widget.'
    nodeName = 'CanvasWidget'

    def __init__(self, name):
        Node.__init__(self, name, terminals={'In': {'io':'in',  'multi':True}})
        self.canvas = None
        self.items = {}

    def disconnected(self, localTerm, remoteTerm):
        if localTerm is self.In:
            if remoteTerm in self.items:
                self.canvas.removeItem(self.items[remoteTerm])
                del self.items[remoteTerm]

    def setCanvas(self, canvas):
        self.canvas = canvas

    def getCanvas(self):
        return self.canvas

    def process(self, In, display=True):
        if display:
            items = set()
            for name, vals in In.items():
                if vals is None:
                    continue
                if type(vals) is not list:
                    vals = [
                     vals]
                for val in vals:
                    vid = id(val)
                    if vid in self.items:
                        items.add(vid)
                    else:
                        self.canvas.addItem(val)
                        item = val
                        self.items[vid] = item
                        items.add(vid)

            for vid in list(self.items.keys()):
                if vid not in items:
                    self.canvas.removeItem(self.items[vid])
                    del self.items[vid]


class PlotCurve(CtrlNode):
    __doc__ = 'Generates a plot curve from x/y data'
    nodeName = 'PlotCurve'
    uiTemplate = [
     ('color', 'color')]

    def __init__(self, name):
        CtrlNode.__init__(self, name, terminals={'x':{'io': 'in'}, 
         'y':{'io': 'in'}, 
         'plot':{'io': 'out'}})
        self.item = PlotDataItem()

    def process(self, x, y, display=True):
        if not display:
            return {'plot': None}
        self.item.setData(x, y, pen=(self.ctrls['color'].color()))
        return {'plot': self.item}


class ScatterPlot(CtrlNode):
    __doc__ = 'Generates a scatter plot from a record array or nested dicts'
    nodeName = 'ScatterPlot'
    uiTemplate = [
     (
      'x', 'combo', {'values':[],  'index':0}),
     (
      'y', 'combo', {'values':[],  'index':0}),
     (
      'sizeEnabled', 'check', {'value': False}),
     (
      'size', 'combo', {'values':[],  'index':0}),
     (
      'absoluteSize', 'check', {'value': False}),
     (
      'colorEnabled', 'check', {'value': False}),
     (
      'color', 'colormap', {}),
     (
      'borderEnabled', 'check', {'value': False}),
     (
      'border', 'colormap', {})]

    def __init__(self, name):
        CtrlNode.__init__(self, name, terminals={'input':{'io': 'in'}, 
         'plot':{'io': 'out'}})
        self.item = ScatterPlotItem()
        self.keys = []

    def process(self, input, display=True):
        if not display:
            return {'plot': None}
        self.updateKeys(input[0])
        x = str(self.ctrls['x'].currentText())
        y = str(self.ctrls['y'].currentText())
        size = str(self.ctrls['size'].currentText())
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
        points = []
        for i in input:
            pt = {'pos': (i[x], i[y])}
            if self.ctrls['sizeEnabled'].isChecked():
                pt['size'] = i[size]
            elif self.ctrls['borderEnabled'].isChecked():
                pt['pen'] = QtGui.QPen(self.ctrls['border'].getColor(i))
            else:
                pt['pen'] = pen
            if self.ctrls['colorEnabled'].isChecked():
                pt['brush'] = QtGui.QBrush(self.ctrls['color'].getColor(i))
            points.append(pt)

        self.item.setPxMode(not self.ctrls['absoluteSize'].isChecked())
        self.item.setPoints(points)
        return {'plot': self.item}

    def updateKeys(self, data):
        if isinstance(data, dict):
            keys = list(data.keys())
        else:
            if isinstance(data, list) or isinstance(data, tuple):
                keys = data
            else:
                if isinstance(data, np.ndarray) or isinstance(data, np.void):
                    keys = data.dtype.names
                else:
                    print('Unknown data type:', type(data), data)
                    return
        for c in self.ctrls.values():
            c.blockSignals(True)

        for c in [self.ctrls['x'], self.ctrls['y'], self.ctrls['size']]:
            cur = str(c.currentText())
            c.clear()
            for k in keys:
                c.addItem(k)
                if k == cur:
                    c.setCurrentIndex(c.count() - 1)

        for c in [self.ctrls['color'], self.ctrls['border']]:
            c.setArgList(keys)

        for c in self.ctrls.values():
            c.blockSignals(False)

        self.keys = keys

    def saveState(self):
        state = CtrlNode.saveState(self)
        return {'keys':self.keys,  'ctrls':state}

    def restoreState(self, state):
        self.updateKeys(state['keys'])
        CtrlNode.restoreState(self, state['ctrls'])
# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/flowchart/library/common.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 5832 bytes
from ...Qt import QtCore, QtGui
import widgets.SpinBox as SpinBox
from ...WidgetGroup import WidgetGroup
from ..Node import Node
import numpy as np
import widgets.ColorButton as ColorButton
try:
    import metaarray
    HAVE_METAARRAY = True
except:
    HAVE_METAARRAY = False

def generateUi(opts):
    """Convenience function for generating common UI types"""
    widget = QtGui.QWidget()
    l = QtGui.QFormLayout()
    l.setSpacing(0)
    widget.setLayout(l)
    ctrls = {}
    row = 0
    for opt in opts:
        if len(opt) == 2:
            k, t = opt
            o = {}
        elif len(opt) == 3:
            k, t, o = opt
        else:
            raise Exception('Widget specification must be (name, type) or (name, type, {opts})')
        if t == 'intSpin':
            w = QtGui.QSpinBox()
            if 'max' in o:
                w.setMaximum(o['max'])
            if 'min' in o:
                w.setMinimum(o['min'])
            if 'value' in o:
                w.setValue(o['value'])
        elif t == 'doubleSpin':
            w = QtGui.QDoubleSpinBox()
            if 'max' in o:
                w.setMaximum(o['max'])
            if 'min' in o:
                w.setMinimum(o['min'])
            if 'value' in o:
                w.setValue(o['value'])
        elif t == 'spin':
            w = SpinBox()
            (w.setOpts)(**o)
        elif t == 'check':
            w = QtGui.QCheckBox()
            if 'checked' in o:
                w.setChecked(o['checked'])
        elif t == 'combo':
            w = QtGui.QComboBox()
            for i in o['values']:
                w.addItem(i)

        elif t == 'color':
            w = ColorButton()
        else:
            raise Exception("Unknown widget type '%s'" % str(t))
        if 'tip' in o:
            w.setToolTip(o['tip'])
        w.setObjectName(k)
        l.addRow(k, w)
        if o.get('hidden', False):
            w.hide()
            label = l.labelForField(w)
            label.hide()
        ctrls[k] = w
        w.rowNum = row
        row += 1

    group = WidgetGroup(widget)
    return (
     widget, group, ctrls)


class CtrlNode(Node):
    """CtrlNode"""
    sigStateChanged = QtCore.Signal(object)

    def __init__(self, name, ui=None, terminals=None):
        if ui is None:
            if hasattr(self, 'uiTemplate'):
                ui = self.uiTemplate
            else:
                ui = []
        if terminals is None:
            terminals = {'In':{'io': 'in'}, 
             'Out':{'io':'out',  'bypass':'In'}}
        Node.__init__(self, name=name, terminals=terminals)
        self.ui, self.stateGroup, self.ctrls = generateUi(ui)
        self.stateGroup.sigChanged.connect(self.changed)

    def ctrlWidget(self):
        return self.ui

    def changed(self):
        self.update()
        self.sigStateChanged.emit(self)

    def process(self, In, display=True):
        out = self.processData(In)
        return {'Out': out}

    def saveState(self):
        state = Node.saveState(self)
        state['ctrl'] = self.stateGroup.state()
        return state

    def restoreState(self, state):
        Node.restoreState(self, state)
        if self.stateGroup is not None:
            self.stateGroup.setState(state.get('ctrl', {}))

    def hideRow(self, name):
        w = self.ctrls[name]
        l = self.ui.layout().labelForField(w)
        w.hide()
        l.hide()

    def showRow(self, name):
        w = self.ctrls[name]
        l = self.ui.layout().labelForField(w)
        w.show()
        l.show()


class PlottingCtrlNode(CtrlNode):
    """PlottingCtrlNode"""

    def __init__(self, name, ui=None, terminals=None):
        CtrlNode.__init__(self, name, ui=ui, terminals=terminals)
        self.plotTerminal = self.addOutput('plot', optional=True)

    def connected(self, term, remote):
        CtrlNode.connected(self, term, remote)
        if term is not self.plotTerminal:
            return
        node = remote.node()
        node.sigPlotChanged.connect(self.connectToPlot)
        self.connectToPlot(node)

    def disconnected(self, term, remote):
        CtrlNode.disconnected(self, term, remote)
        if term is not self.plotTerminal:
            return
        remote.node().sigPlotChanged.disconnect(self.connectToPlot)
        self.disconnectFromPlot(remote.node().getPlot())

    def connectToPlot(self, node):
        """Define what happens when the node is connected to a plot"""
        raise Exception('Must be re-implemented in subclass')

    def disconnectFromPlot(self, plot):
        """Define what happens when the node is disconnected from a plot"""
        raise Exception('Must be re-implemented in subclass')

    def process(self, In, display=True):
        out = CtrlNode.process(self, In, display)
        out['plot'] = None
        return out


def metaArrayWrapper(fn):

    def newFn(self, data, *args, **kargs):
        if HAVE_METAARRAY:
            if hasattr(data, 'implements'):
                if data.implements('MetaArray'):
                    d1 = fn(self, data.view(np.ndarray), *args, **kargs)
                    info = data.infoCopy()
                    if d1.shape != data.shape:
                        for i in range(data.ndim):
                            if 'values' in info[i]:
                                info[i]['values'] = info[i]['values'][:d1.shape[i]]

                    return metaarray.MetaArray(d1, info=info)
        return fn(self, data, *args, **kargs)

    return newFn
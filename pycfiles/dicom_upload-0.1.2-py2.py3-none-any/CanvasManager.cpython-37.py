# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/canvas/CanvasManager.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2206 bytes
from ..Qt import QtCore, QtGui
if not hasattr(QtCore, 'Signal'):
    QtCore.Signal = QtCore.pyqtSignal
import weakref

class CanvasManager(QtCore.QObject):
    SINGLETON = None
    sigCanvasListChanged = QtCore.Signal()

    def __init__(self):
        if CanvasManager.SINGLETON is not None:
            raise Exception('Can only create one canvas manager.')
        CanvasManager.SINGLETON = self
        QtCore.QObject.__init__(self)
        self.canvases = weakref.WeakValueDictionary()

    @classmethod
    def instance(cls):
        return CanvasManager.SINGLETON

    def registerCanvas(self, canvas, name):
        n2 = name
        i = 0
        while n2 in self.canvases:
            n2 = '%s_%03d' % (name, i)
            i += 1

        self.canvases[n2] = canvas
        self.sigCanvasListChanged.emit()
        return n2

    def unregisterCanvas(self, name):
        c = self.canvases[name]
        del self.canvases[name]
        self.sigCanvasListChanged.emit()

    def listCanvases(self):
        return list(self.canvases.keys())

    def getCanvas(self, name):
        return self.canvases[name]


manager = CanvasManager()

class CanvasCombo(QtGui.QComboBox):

    def __init__(self, parent=None):
        QtGui.QComboBox.__init__(self, parent)
        man = CanvasManager.instance()
        man.sigCanvasListChanged.connect(self.updateCanvasList)
        self.hostName = None
        self.updateCanvasList()

    def updateCanvasList(self):
        canvases = CanvasManager.instance().listCanvases()
        canvases.insert(0, '')
        if self.hostName in canvases:
            canvases.remove(self.hostName)
        sel = self.currentText()
        if sel in canvases:
            self.blockSignals(True)
        self.clear()
        for i in canvases:
            self.addItem(i)
            if i == sel:
                self.setCurrentIndex(self.count())

        self.blockSignals(False)

    def setHostName(self, name):
        self.hostName = name
        self.updateCanvasList()
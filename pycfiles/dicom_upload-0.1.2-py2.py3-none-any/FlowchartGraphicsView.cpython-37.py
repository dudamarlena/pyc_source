# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/flowchart/FlowchartGraphicsView.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 3857 bytes
from ..Qt import QtGui, QtCore
import widgets.GraphicsView as GraphicsView
from ..GraphicsScene import GraphicsScene
import graphicsItems.ViewBox as ViewBox

class FlowchartGraphicsView(GraphicsView):
    sigHoverOver = QtCore.Signal(object)
    sigClicked = QtCore.Signal(object)

    def __init__(self, widget, *args):
        (GraphicsView.__init__)(self, *args, **{'useOpenGL': False})
        self._vb = FlowchartViewBox(widget, lockAspect=True, invertY=True)
        self.setCentralItem(self._vb)
        self.setRenderHint(QtGui.QPainter.Antialiasing, True)

    def viewBox(self):
        return self._vb


class FlowchartViewBox(ViewBox):

    def __init__(self, widget, *args, **kwargs):
        (ViewBox.__init__)(self, *args, **kwargs)
        self.widget = widget

    def getMenu(self, ev):
        self._fc_menu = QtGui.QMenu()
        self._subMenus = self.getContextMenus(ev)
        for menu in self._subMenus:
            self._fc_menu.addMenu(menu)

        return self._fc_menu

    def getContextMenus(self, ev):
        menu = self.widget.buildMenu(ev.scenePos())
        menu.setTitle('Add node')
        return [
         menu, ViewBox.getMenu(self, ev)]
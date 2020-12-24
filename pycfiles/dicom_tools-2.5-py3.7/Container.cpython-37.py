# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/dockarea/Container.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 8634 bytes
from ..Qt import QtCore, QtGui
import weakref

class Container(object):

    def __init__(self, area):
        object.__init__(self)
        self.area = area
        self._container = None
        self._stretch = (10, 10)
        self.stretches = weakref.WeakKeyDictionary()

    def container(self):
        return self._container

    def containerChanged(self, c):
        self._container = c

    def type(self):
        pass

    def insert(self, new, pos=None, neighbor=None):
        new.setParent(None)
        if not isinstance(new, list):
            new = [
             new]
        if neighbor is None:
            if pos == 'before':
                index = 0
            else:
                index = self.count()
        else:
            index = self.indexOf(neighbor)
            if index == -1:
                index = 0
            if pos == 'after':
                index += 1
        for n in new:
            n.containerChanged(self)
            self._insertItem(n, index)
            index += 1
            n.sigStretchChanged.connect(self.childStretchChanged)

        self.updateStretch()

    def apoptose(self, propagate=True):
        cont = self._container
        c = self.count()
        if c > 1:
            return
        if self.count() == 1:
            if self is self.area.topContainer:
                return
            self.container().insert(self.widget(0), 'before', self)
        self.close()
        if propagate:
            if cont is not None:
                cont.apoptose()

    def close(self):
        self.area = None
        self._container = None
        self.setParent(None)

    def childEvent(self, ev):
        ch = ev.child()
        if ev.removed():
            if hasattr(ch, 'sigStretchChanged'):
                try:
                    ch.sigStretchChanged.disconnect(self.childStretchChanged)
                except:
                    pass

                self.updateStretch()

    def childStretchChanged(self):
        self.updateStretch()

    def setStretch(self, x=None, y=None):
        self._stretch = (
         x, y)
        self.sigStretchChanged.emit()

    def updateStretch(self):
        pass

    def stretch(self):
        """Return the stretch factors for this container"""
        return self._stretch


class SplitContainer(Container, QtGui.QSplitter):
    __doc__ = 'Horizontal or vertical splitter with some changes:\n     - save/restore works correctly\n    '
    sigStretchChanged = QtCore.Signal()

    def __init__(self, area, orientation):
        QtGui.QSplitter.__init__(self)
        self.setOrientation(orientation)
        Container.__init__(self, area)

    def _insertItem(self, item, index):
        self.insertWidget(index, item)
        item.show()

    def saveState(self):
        sizes = self.sizes()
        if all([x == 0 for x in sizes]):
            sizes = [
             10] * len(sizes)
        return {'sizes': sizes}

    def restoreState(self, state):
        sizes = state['sizes']
        self.setSizes(sizes)
        for i in range(len(sizes)):
            self.setStretchFactor(i, sizes[i])

    def childEvent(self, ev):
        QtGui.QSplitter.childEvent(self, ev)
        Container.childEvent(self, ev)


class HContainer(SplitContainer):

    def __init__(self, area):
        SplitContainer.__init__(self, area, QtCore.Qt.Horizontal)

    def type(self):
        return 'horizontal'

    def updateStretch(self):
        x = 0
        y = 0
        sizes = []
        for i in range(self.count()):
            wx, wy = self.widget(i).stretch()
            x += wx
            y = max(y, wy)
            sizes.append(wx)

        self.setStretch(x, y)
        tot = float(sum(sizes))
        if tot == 0:
            scale = 1.0
        else:
            scale = self.width() / tot
        self.setSizes([int(s * scale) for s in sizes])


class VContainer(SplitContainer):

    def __init__(self, area):
        SplitContainer.__init__(self, area, QtCore.Qt.Vertical)

    def type(self):
        return 'vertical'

    def updateStretch(self):
        x = 0
        y = 0
        sizes = []
        for i in range(self.count()):
            wx, wy = self.widget(i).stretch()
            y += wy
            x = max(x, wx)
            sizes.append(wy)

        self.setStretch(x, y)
        tot = float(sum(sizes))
        if tot == 0:
            scale = 1.0
        else:
            scale = self.height() / tot
        self.setSizes([int(s * scale) for s in sizes])


class TContainer(Container, QtGui.QWidget):
    sigStretchChanged = QtCore.Signal()

    def __init__(self, area):
        QtGui.QWidget.__init__(self)
        Container.__init__(self, area)
        self.layout = QtGui.QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.hTabLayout = QtGui.QHBoxLayout()
        self.hTabBox = QtGui.QWidget()
        self.hTabBox.setLayout(self.hTabLayout)
        self.hTabLayout.setSpacing(2)
        self.hTabLayout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.hTabBox, 0, 1)
        self.stack = QtGui.QStackedWidget()
        self.layout.addWidget(self.stack, 1, 1)
        self.stack.childEvent = self.stackChildEvent
        self.setLayout(self.layout)
        for n in ('count', 'widget', 'indexOf'):
            setattr(self, n, getattr(self.stack, n))

    def _insertItem(self, item, index):
        if not isinstance(item, Dock.Dock):
            raise Exception('Tab containers may hold only docks, not other containers.')
        self.stack.insertWidget(index, item)
        self.hTabLayout.insertWidget(index, item.label)
        item.label.sigClicked.connect(self.tabClicked)
        self.tabClicked(item.label)

    def tabClicked(self, tab, ev=None):
        if ev is None or ev.button() == QtCore.Qt.LeftButton:
            for i in range(self.count()):
                w = self.widget(i)
                if w is tab.dock:
                    w.label.setDim(False)
                    self.stack.setCurrentIndex(i)
                else:
                    w.label.setDim(True)

    def raiseDock(self, dock):
        """Move *dock* to the top of the stack"""
        self.stack.currentWidget().label.setDim(True)
        self.stack.setCurrentWidget(dock)
        dock.label.setDim(False)

    def type(self):
        return 'tab'

    def saveState(self):
        return {'index': self.stack.currentIndex()}

    def restoreState(self, state):
        self.stack.setCurrentIndex(state['index'])

    def updateStretch(self):
        x = 0
        y = 0
        for i in range(self.count()):
            wx, wy = self.widget(i).stretch()
            x = max(x, wx)
            y = max(y, wy)

        self.setStretch(x, y)

    def stackChildEvent(self, ev):
        QtGui.QStackedWidget.childEvent(self.stack, ev)
        Container.childEvent(self, ev)


from . import Dock
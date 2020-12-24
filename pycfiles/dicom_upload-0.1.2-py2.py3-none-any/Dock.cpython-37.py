# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/dockarea/Dock.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 12077 bytes
from ..Qt import QtCore, QtGui
from .DockDrop import *
import widgets.VerticalLabel as VerticalLabel
from ..python2_3 import asUnicode

class Dock(QtGui.QWidget, DockDrop):
    sigStretchChanged = QtCore.Signal()
    sigClosed = QtCore.Signal(object)

    def __init__(self, name, area=None, size=(10, 10), widget=None, hideTitle=False, autoOrientation=True, closable=False):
        QtGui.QWidget.__init__(self)
        DockDrop.__init__(self)
        self._container = None
        self._name = name
        self.area = area
        self.label = DockLabel(name, self, closable)
        if closable:
            self.label.sigCloseClicked.connect(self.close)
        self.labelHidden = False
        self.moveLabel = True
        self.autoOrient = autoOrientation
        self.orientation = 'horizontal'
        self.topLayout = QtGui.QGridLayout()
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.setSpacing(0)
        self.setLayout(self.topLayout)
        self.topLayout.addWidget(self.label, 0, 1)
        self.widgetArea = QtGui.QWidget()
        self.topLayout.addWidget(self.widgetArea, 1, 1)
        self.layout = QtGui.QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.widgetArea.setLayout(self.layout)
        self.widgetArea.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.widgets = []
        self.currentRow = 0
        self.raiseOverlay()
        self.hStyle = '\n        Dock > QWidget {\n            border: 1px solid #000;\n            border-radius: 5px;\n            border-top-left-radius: 0px;\n            border-top-right-radius: 0px;\n            border-top-width: 0px;\n        }'
        self.vStyle = '\n        Dock > QWidget {\n            border: 1px solid #000;\n            border-radius: 5px;\n            border-top-left-radius: 0px;\n            border-bottom-left-radius: 0px;\n            border-left-width: 0px;\n        }'
        self.nStyle = '\n        Dock > QWidget {\n            border: 1px solid #000;\n            border-radius: 5px;\n        }'
        self.dragStyle = '\n        Dock > QWidget {\n            border: 4px solid #00F;\n            border-radius: 5px;\n        }'
        self.setAutoFillBackground(False)
        self.widgetArea.setStyleSheet(self.hStyle)
        (self.setStretch)(*size)
        if widget is not None:
            self.addWidget(widget)
        if hideTitle:
            self.hideTitleBar()

    def implements(self, name=None):
        if name is None:
            return ['dock']
        return name == 'dock'

    def setStretch(self, x=None, y=None):
        """
        Set the 'target' size for this Dock.
        The actual size will be determined by comparing this Dock's
        stretch value to the rest of the docks it shares space with.
        """
        if x is None:
            x = 0
        if y is None:
            y = 0
        self._stretch = (
         x, y)
        self.sigStretchChanged.emit()

    def stretch(self):
        return self._stretch

    def hideTitleBar(self):
        """
        Hide the title bar for this Dock.
        This will prevent the Dock being moved by the user.
        """
        self.label.hide()
        self.labelHidden = True
        if 'center' in self.allowedAreas:
            self.allowedAreas.remove('center')
        self.updateStyle()

    def showTitleBar(self):
        """
        Show the title bar for this Dock.
        """
        self.label.show()
        self.labelHidden = False
        self.allowedAreas.add('center')
        self.updateStyle()

    def title(self):
        """
        Gets the text displayed in the title bar for this dock.
        """
        return asUnicode(self.label.text())

    def setTitle(self, text):
        """
        Sets the text displayed in title bar for this Dock.
        """
        self.label.setText(text)

    def setOrientation(self, o='auto', force=False):
        """
        Sets the orientation of the title bar for this Dock.
        Must be one of 'auto', 'horizontal', or 'vertical'.
        By default ('auto'), the orientation is determined
        based on the aspect ratio of the Dock.
        """
        if o == 'auto':
            if self.autoOrient:
                if self.container().type() == 'tab':
                    o = 'horizontal'
                elif self.width() > self.height() * 1.5:
                    o = 'vertical'
                else:
                    o = 'horizontal'
        if force or self.orientation != o:
            self.orientation = o
            self.label.setOrientation(o)
            self.updateStyle()

    def updateStyle(self):
        if self.labelHidden:
            self.widgetArea.setStyleSheet(self.nStyle)
        elif self.orientation == 'vertical':
            self.label.setOrientation('vertical')
            if self.moveLabel:
                self.topLayout.addWidget(self.label, 1, 0)
            self.widgetArea.setStyleSheet(self.vStyle)
        else:
            self.label.setOrientation('horizontal')
            if self.moveLabel:
                self.topLayout.addWidget(self.label, 0, 1)
            self.widgetArea.setStyleSheet(self.hStyle)

    def resizeEvent(self, ev):
        self.setOrientation()
        self.resizeOverlay(self.size())

    def name(self):
        return self._name

    def container(self):
        return self._container

    def addWidget(self, widget, row=None, col=0, rowspan=1, colspan=1):
        """
        Add a new widget to the interior of this Dock.
        Each Dock uses a QGridLayout to arrange widgets within.
        """
        if row is None:
            row = self.currentRow
        self.currentRow = max(row + 1, self.currentRow)
        self.widgets.append(widget)
        self.layout.addWidget(widget, row, col, rowspan, colspan)
        self.raiseOverlay()

    def startDrag(self):
        self.drag = QtGui.QDrag(self)
        mime = QtCore.QMimeData()
        self.drag.setMimeData(mime)
        self.widgetArea.setStyleSheet(self.dragStyle)
        self.update()
        action = self.drag.exec_()
        self.updateStyle()

    def float(self):
        self.area.floatDock(self)

    def containerChanged(self, c):
        self._container = c
        if c.type() != 'tab':
            self.moveLabel = True
            self.label.setDim(False)
        else:
            self.moveLabel = False
        self.setOrientation(force=True)

    def raiseDock(self):
        """If this Dock is stacked underneath others, raise it to the top."""
        self.container().raiseDock(self)

    def close(self):
        """Remove this dock from the DockArea it lives inside."""
        self.setParent(None)
        self.label.setParent(None)
        self._container.apoptose()
        self._container = None
        self.sigClosed.emit(self)

    def __repr__(self):
        return '<Dock %s %s>' % (self.name(), self.stretch())

    def dragEnterEvent(self, *args):
        (DockDrop.dragEnterEvent)(self, *args)

    def dragMoveEvent(self, *args):
        (DockDrop.dragMoveEvent)(self, *args)

    def dragLeaveEvent(self, *args):
        (DockDrop.dragLeaveEvent)(self, *args)

    def dropEvent(self, *args):
        (DockDrop.dropEvent)(self, *args)


class DockLabel(VerticalLabel):
    sigClicked = QtCore.Signal(object, object)
    sigCloseClicked = QtCore.Signal()

    def __init__(self, text, dock, showCloseButton):
        self.dim = False
        self.fixedWidth = False
        VerticalLabel.__init__(self, text, orientation='horizontal', forceWidth=False)
        self.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.dock = dock
        self.updateStyle()
        self.setAutoFillBackground(False)
        self.startedDrag = False
        self.closeButton = None
        if showCloseButton:
            self.closeButton = QtGui.QToolButton(self)
            self.closeButton.clicked.connect(self.sigCloseClicked)
            self.closeButton.setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_TitleBarCloseButton))

    def updateStyle(self):
        r = '3px'
        if self.dim:
            fg = '#aaa'
            bg = '#44a'
            border = '#339'
        else:
            fg = '#fff'
            bg = '#66c'
            border = '#55B'
        if self.orientation == 'vertical':
            self.vStyle = 'DockLabel {\n                background-color : %s;\n                color : %s;\n                border-top-right-radius: 0px;\n                border-top-left-radius: %s;\n                border-bottom-right-radius: 0px;\n                border-bottom-left-radius: %s;\n                border-width: 0px;\n                border-right: 2px solid %s;\n                padding-top: 3px;\n                padding-bottom: 3px;\n            }' % (bg, fg, r, r, border)
            self.setStyleSheet(self.vStyle)
        else:
            self.hStyle = 'DockLabel {\n                background-color : %s;\n                color : %s;\n                border-top-right-radius: %s;\n                border-top-left-radius: %s;\n                border-bottom-right-radius: 0px;\n                border-bottom-left-radius: 0px;\n                border-width: 0px;\n                border-bottom: 2px solid %s;\n                padding-left: 3px;\n                padding-right: 3px;\n            }' % (bg, fg, r, r, border)
            self.setStyleSheet(self.hStyle)

    def setDim(self, d):
        if self.dim != d:
            self.dim = d
            self.updateStyle()

    def setOrientation(self, o):
        VerticalLabel.setOrientation(self, o)
        self.updateStyle()

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            self.pressPos = ev.pos()
            self.startedDrag = False
            ev.accept()

    def mouseMoveEvent(self, ev):
        if not self.startedDrag:
            if (ev.pos() - self.pressPos).manhattanLength() > QtGui.QApplication.startDragDistance():
                self.dock.startDrag()
        ev.accept()

    def mouseReleaseEvent(self, ev):
        if not self.startedDrag:
            self.sigClicked.emit(self, ev)
        ev.accept()

    def mouseDoubleClickEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            self.dock.float()

    def resizeEvent(self, ev):
        if self.closeButton:
            if self.orientation == 'vertical':
                size = ev.size().width()
                pos = QtCore.QPoint(0, 0)
            else:
                size = ev.size().height()
                pos = QtCore.QPoint(ev.size().width() - size, 0)
            self.closeButton.setFixedSize(QtCore.QSize(size, size))
            self.closeButton.move(pos)
        super(DockLabel, self).resizeEvent(ev)
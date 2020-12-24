# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/bibolamazi_gui/overlistbuttonwidget.py
# Compiled at: 2015-05-11 05:40:29
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import bibolamazi.init
from .qtauto.ui_overlistbuttonwidget import Ui_OverListButtonWidget
ROLE_OVERBUTTON = Qt.UserRole + 137
OVERBUTTON_NONE = 0
OVERBUTTON_ADD = 1
OVERBUTTON_REMOVE = 2
ROLE_ARGNAME = Qt.UserRole + 138

class OverListButtonWidgetBase(QWidget):

    def __init__(self, itemview):
        super(OverListButtonWidgetBase, self).__init__(itemview.viewport())
        self.hide()
        self._view = itemview
        self._view_viewport = self._view.viewport()
        self._view_viewport.setMouseTracking(True)
        self._view_viewport.installEventFilter(self)
        self._lastpos = None
        self._curidx = None
        return

    def curIndex(self):
        return self._curidx

    def itemView(self):
        return self._view

    def eventFilter(self, obj, event):
        if obj == self._view_viewport:
            if event.type() == QEvent.FocusOut:
                self.hide()
            if event.type() == QEvent.MouseMove:
                self.updateDisplay(event.pos())
            if event.type() == QEvent.Leave:
                self.updateDisplay(False)
        return super(OverListButtonWidgetBase, self).eventFilter(obj, event)

    @pyqtSlot()
    def updateDisplay(self, pos=None):
        if pos is None:
            pos = self._lastpos
        elif pos is False:
            pos = None
        self._lastpos = pos
        if pos is None:
            self._disappear()
            return
        else:
            idx = self._view.indexAt(pos)
            if self.show_status(idx):
                self._appear(idx)
                return True
            self._disappear()
            return False

    def show_status(self, index):
        return False

    def _disappear(self):
        self._curidx = None
        self.hide()
        return

    def _appear(self, idx):
        self.show()
        self.setGeometry(self.get_widget_rect(self._view.visualRect(idx)))
        self._curidx = idx

    def get_widget_rect(self, rect):
        rect2 = QRect(rect)
        sh = self.minimumSizeHint()
        rect2.setLeft(rect.right() - sh.width())
        return rect2


class OverListButtonWidget(OverListButtonWidgetBase):

    def __init__(self, itemview):
        super(OverListButtonWidget, self).__init__(itemview)
        self.ui = Ui_OverListButtonWidget()
        self.ui.setupUi(self)

    addClicked = pyqtSignal('QString')
    editClicked = pyqtSignal('QString')
    removeClicked = pyqtSignal('QString')
    addIndexClicked = pyqtSignal('QModelIndex')
    editIndexClicked = pyqtSignal('QModelIndex')
    removeIndexClicked = pyqtSignal('QModelIndex')

    def show_status(self, idx):
        if not idx.isValid():
            return False
        v = idx.data(ROLE_OVERBUTTON)
        if not v.isValid():
            return False
        whichbtn = v.toPyObject()
        if whichbtn == OVERBUTTON_ADD:
            self.ui.btnAdd.show()
            self.ui.btnEdit.hide()
            self.ui.btnRemove.hide()
            return True
        if whichbtn == OVERBUTTON_REMOVE:
            self.ui.btnAdd.hide()
            self.ui.btnEdit.show()
            self.ui.btnRemove.show()
            return True
        return False

    @pyqtSlot()
    def on_btnAdd_clicked(self):
        curidx = self.curIndex()
        if curidx is None:
            return
        else:
            self.addIndexClicked.emit(curidx)
            self.addClicked.emit(curidx.data(ROLE_ARGNAME).toString())
            return

    @pyqtSlot()
    def on_btnEdit_clicked(self):
        curidx = self.curIndex()
        if curidx is None:
            return
        else:
            self.editIndexClicked.emit(curidx)
            self.editClicked.emit(curidx.data(ROLE_ARGNAME).toString())
            return

    @pyqtSlot()
    def on_btnRemove_clicked(self):
        curidx = self.curIndex()
        if curidx is None:
            return
        else:
            self.removeIndexClicked.emit(curidx)
            self.removeClicked.emit(curidx.data(ROLE_ARGNAME).toString())
            return
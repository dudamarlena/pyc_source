# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpQtLib/widgets/balloon.py
# Compiled at: 2020-01-16 21:52:29
# Size of source mod 2**32: 3090 bytes
"""
Collapsible accordion widget similar to Maya Attribute Editor
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtGui import *

class BalloonDialog(QDialog, object):
    FIXED_HEIGHT = 15
    FIXED_WIDTH = 35

    class BallonDialogFocuser(QWidget, object):

        def __init__(self, w):
            super(BalloonDialog.BallonDialogFocuser, self).__init__()
            self._widget = w

        def show(self):
            """
            Overrides base QWidget show function
            """
            self._widget.show()
            self.focus()

        def focus(self):
            """
            Function that focus wrapped widget
            """
            self._widget.activateWindow()
            self._widget.raise_()

    def __init__(self, modal=False, parent=None):
        super(BalloonDialog, self).__init__(parent)
        self._lazy_show_window = QTimer(self)
        if modal:
            self.setModal(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self._lazy_show_window.timeout.connect(self._on_lazy_show_window)

    def resizeEvent(self, event):
        """
        Overrides base QDialog resizeEvent function
        :param event: QResizeEvent
        """
        r = self.rect()
        ss = self.styleSheet()
        self.setStyleSheet('{} margin-top: {}px;'.format(ss, self.FIXED_HEIGHT))
        poly = QPolygon()
        poly.append(QPoint(r.x(), r.y() + self.FIXED_HEIGHT))
        poly.append(QPoint(r.x() + r.width() / 2 - self.FIXED_WIDTH / 2, r.y() + self.FIXED_HEIGHT))
        poly.append(QPoint(r.x() + r.width() / 2, r.y()))
        poly.append(QPoint(r.x() + r.width() / 2 + self.FIXED_WIDTH / 2, r.y() + self.FIXED_HEIGHT))
        poly.append(QPoint(r.x() + r.width(), r.y() + self.FIXED_HEIGHT))
        poly.append(QPoint(r.x() + r.width(), r.y() + r.height()))
        poly.append(QPoint(r.x(), r.y() + r.height()))
        new_mask = QRegion(poly)
        self.setMask(new_mask)

    def event(self, e):
        if QEvent.WindowDeactivate == e.type():
            self.done(False)
            e.ignore()
            return True
        else:
            return super(BalloonDialog, self).event(e)

    def focusOutEvent(self, event):
        """
        Overrides base QDialog focusOutEvent function
        :param event: QFocusEven
        """
        pass

    def showEvent(self, event):
        """
        Overrides base QDialog showEvent function
        :param event: QShowEvent
        """
        focuser = BalloonDialog.BallonDialogFocuser(self)
        focuser.focus()

    def _on_lazy_show_window(self):
        """
        Internal callback function that is called when lazy show window timer finishes
        """
        self.activateWindow()
        self.setFocus()
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/widgets/tab_bar.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 961 bytes
"""
This module contains the tab bar used in the splittable tab widget.
"""
from pyqode.qt import QtWidgets, QtCore
from pyqode.core.api import DelayJobRunner

class TabBar(QtWidgets.QTabBar):
    __doc__ = '\n    Tab bar specialized to allow the user to close a tab using mouse middle\n    click. Also exposes a double clicked signal.\n    '
    double_clicked = QtCore.Signal()

    def __init__(self, parent):
        QtWidgets.QTabBar.__init__(self, parent)
        self.setTabsClosable(True)
        self._timer = DelayJobRunner(delay=1)

    def mousePressEvent(self, event):
        QtWidgets.QTabBar.mousePressEvent(self, event)
        if event.button() == QtCore.Qt.MiddleButton:
            tab = self.tabAt(event.pos())
            self._timer.request_job(self.parentWidget().tabCloseRequested.emit, tab)

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.double_clicked.emit()
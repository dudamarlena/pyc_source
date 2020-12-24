# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/ListWidgets/ROIItemModule.py
# Compiled at: 2020-04-22 19:12:53
# Size of source mod 2**32: 1570 bytes
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtCore

class ROIItemModule(QStandardItem):

    def __init__(self, color, num, roi_tab):
        self.roi_tab = roi_tab
        out_img = QImage(100, 100, QImage.Format_ARGB32)
        out_img.fill(Qt.transparent)
        brush = QBrush(QColor(*color))
        painter = QPainter(out_img)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawEllipse(0, 0, 100, 100)
        painter.end()
        pr = QWindow().devicePixelRatio()
        pm = QPixmap.fromImage(out_img)
        self.num = num
        super().__init__(pm, '')
        self.setEditable(False)

    def toggle_check_state(self):
        if self.checkState() == False:
            self.roi_tab.selectRoi(self.num)
            self.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            self.roi_tab.deselectRoi(self.num)
            self.setCheckState(QtCore.Qt.CheckState.Unchecked)

    def checkState(self):
        state = super().checkState()
        if state == QtCore.Qt.CheckState.Unchecked:
            return False
        return True
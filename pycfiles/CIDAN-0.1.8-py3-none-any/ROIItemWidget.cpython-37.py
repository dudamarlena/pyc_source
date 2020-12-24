# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/ListWidgets/ROIItemWidget.py
# Compiled at: 2020-04-29 15:48:11
# Size of source mod 2**32: 4766 bytes
from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class ROIItemWidget(QWidget):

    def __init__(self, roi_tab, color, roi_list, roi_num, parent=None):
        self.roi_tab = roi_tab
        self.roi_list = roi_list
        self.roi_num = roi_num
        super(ROIItemWidget, self).__init__(parent)
        self.setStyleSheet('QPushButton {background-color: rgba(0,0,0,0%);\n        padding-left:3px;\n        padding-right:3px;\n        \n        color: #CCCCCC;}\n        QPushButton:hover {\n          border: 1px solid #148CD2;\n          background-color: #505F69;\n          color: #F0F0F0;\n            }\n            QPushButton:pressed {\n  background-color: #19232D;\n  border: 1px solid #19232D;\n}\n\nQPushButton:pressed:hover {\n  border: 1px solid #148CD2;\n}\nQPushButton:selected {\n  background-color: rgba(0,0,0,0%);\n  color: #32414B;\n}\n            QLabel {\n            background-color: rgba(0,0,0,0%)\n            }QCheckBox {\n            background-color: rgba(0,0,0,0%)\n            }')
        self.zoom_button = QPushButton('Zoom To')
        self.zoom_button.clicked.connect(lambda x: self.roi_tab.zoomRoi(self.roi_num))
        self.check_box = QCheckBox()
        self.check_box.toggled.connect(lambda : self.check_box_toggled())
        self.check_box_time_trace = QCheckBox()
        self.check_box_time_trace.toggled.connect(lambda : self.time_check_box_toggled())
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
        label_pix = QLabel()
        label_pix.setPixmap(pm)
        label_pix.setMaximumWidth(10)
        lay = QtGui.QHBoxLayout(self)
        lay.addWidget((self.check_box), alignment=(QtCore.Qt.AlignLeft))
        lay.addWidget(QLabel(text=('#' + str(roi_num))), alignment=(QtCore.Qt.AlignLeft))
        lay.addWidget(QLabel())
        lay.addWidget(QLabel())
        lay.addWidget(QLabel())
        lay.addWidget(QLabel())
        lay.addWidget((self.zoom_button), alignment=(QtCore.Qt.AlignRight))
        lay.addWidget((self.check_box_time_trace), alignment=(QtCore.Qt.AlignRight))
        lay.setContentsMargins(0, 0, 0, 0)

    def select_check_box(self):
        if not self.check_box.checkState():
            for x in self.roi_list.roi_item_list:
                if x != self:
                    x.check_box.setChecked(False)

            self.check_box.setChecked(True)
            self.roi_list.current_selected_roi = self.roi_num
        else:
            self.check_box.setChecked(False)
            self.roi_list.current_selected_roi = None

    def select_time_check_box(self):
        self.check_box_time_trace.setChecked(not self.check_box_time_trace.checkState())

    def check_box_toggled(self):
        if self.check_box.checkState():
            self.roi_tab.selectRoi(self.roi_num)
            for x in self.roi_list.roi_item_list:
                if x != self:
                    x.check_box.setChecked(False)

            self.roi_list.current_selected_roi = self.roi_num
        else:
            self.roi_list.current_selected_roi = None
            self.roi_tab.deselectRoi(self.roi_num)

    def time_check_box_toggled(self):
        self.roi_list.roi_time_check_list[self.roi_num - 1] = self.check_box_time_trace.checkState()
        if self.check_box_time_trace.checkState():
            self.roi_tab.selectRoiTime(self.roi_num)
        else:
            self.roi_tab.deselectRoiTime(self.roi_num)
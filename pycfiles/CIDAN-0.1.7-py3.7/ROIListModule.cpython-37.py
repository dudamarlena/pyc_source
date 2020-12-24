# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/ListWidgets/ROIListModule.py
# Compiled at: 2020-04-29 15:33:10
# Size of source mod 2**32: 3403 bytes
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtCore
import CIDAN.GUI.ListWidgets.ROIItemModule as ROIItemModule
import CIDAN.GUI.ListWidgets.ROIItemWidget as ROIItemWidget

class ROIListModule(QFrame):

    def __init__(self, data_handler, roi_tab):
        super().__init__()
        self.current_selected_roi = 0
        self.roi_tab = roi_tab
        self.color_list = data_handler.color_list
        self.list = QListView()
        self.setStyleSheet('QListView::item { border-bottom: 1px solid rgb(50, 65, 75); }')
        self.top_labels_layout = QHBoxLayout()
        label1 = QLabel(text='ROI Selected')
        label1.setMaximumWidth(100)
        self.top_labels_layout.addWidget(label1, alignment=(QtCore.Qt.AlignRight))
        label2 = QLabel(text='ROI Num')
        label2.setMaximumWidth(100)
        self.top_labels_layout.addWidget(label2, alignment=(QtCore.Qt.AlignLeft))
        self.top_labels_layout.addWidget((QLabel()), alignment=(QtCore.Qt.AlignRight))
        self.top_labels_layout.addWidget((QLabel()), alignment=(QtCore.Qt.AlignRight))
        self.top_labels_layout.addWidget((QLabel()), alignment=(QtCore.Qt.AlignRight))
        self.top_labels_layout.addWidget((QLabel()), alignment=(QtCore.Qt.AlignRight))
        label3 = QLabel(text='Time Trace On')
        label3.setMaximumWidth(100)
        self.top_labels_layout.addWidget(label3, alignment=(QtCore.Qt.AlignRight))
        self.model = QStandardItemModel(self.list)
        self.list.setModel(self.model)
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.top_labels_layout)
        self.layout.addWidget(self.list)
        self.roi_item_list = []
        self.setLayout(self.layout)

    def set_current_select(self, num):
        self.list.setCurrentIndex(self.model.index(int(num - 1), 0))
        self.roi_time_check_list[num - 1] = not self.roi_time_check_list[(num - 1)]
        self.roi_item_list[(num - 1)].select_check_box()
        self.roi_item_list[(num - 1)].select_time_check_box()

    def set_list_items(self, clusters):
        self.cluster_list = clusters
        for x in range(self.model.rowCount()):
            self.model.removeRow(0)

        self.roi_item_list = []
        for num in range(len(self.cluster_list)):
            item = ROIItemWidget(self.roi_tab, self.color_list[(num % len(self.color_list))], self, num + 1)
            item1 = ROIItemModule(self.color_list[(num % len(self.color_list))], num + 1, self.roi_tab)
            self.roi_item_list.append(item)
            self.model.appendRow(item1)
            self.list.setIndexWidget(item1.index(), item)

        self.roi_time_check_list = [
         False] * len(self.roi_item_list)
        self.roi_item_list[0].select_check_box()
        self.roi_item_list[0].select_time_check_box()
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/table.py
# Compiled at: 2019-10-29 13:45:26
# Size of source mod 2**32: 2261 bytes
from PyQt5.QtWidgets import QTableView, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt
STRETCH = QHeaderView.Stretch

class TableView(QTableView):

    def __init__(self, name, model, col_sizes=[], method_selected_row=None):
        super(TableView, self).__init__()
        self.setObjectName(name)
        self.verticalHeader().hide()
        self.setGridStyle(Qt.DotLine)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.model = model
        self.method_selected_row = method_selected_row
        self.doubleClicked.connect(self.on_selected_row)
        self.setWordWrap(False)
        if model:
            self.setModel(model)
        header = self.horizontalHeader()
        if col_sizes:
            for i, size in enumerate(col_sizes):
                if type(size) == int:
                    header.resizeSection(i, size)
                else:
                    header.setSectionResizeMode(i, STRETCH)

    def on_selected_row(self):
        selected_idx = self.currentIndex()
        if selected_idx:
            self.method_selected_row(self.model.get_data(selected_idx))

    def rowsInserted(self, index, start, end):
        self.scrollToBottom()

    def removeElement(self, index):
        if not index:
            return
        if index.row() >= 0:
            if self.hasFocus():
                item = self.model.get_data(index)
                id_ = self.model.removeId(index.row(), index)
                self.model.deleteRecords([id_])
                self.model.layoutChanged.emit()
                return item

    def delete_item(self):
        item_removed = {}
        selected_idx = self.currentIndex()
        item_removed = self.removeElement(selected_idx)
        return item_removed

    def moved_selection(self, key):
        selected_idx = self.currentIndex()
        if key == Qt.Key_Down:
            self.selectRow(selected_idx.row() + 1)
        else:
            if key == Qt.Key_Up:
                self.selectRow(selected_idx.row() - 1)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pySPM\tools\values_display.py
# Compiled at: 2019-05-21 08:54:40
# Size of source mod 2**32: 1177 bytes
"""
This module allows to display a small GUI in order to display a table of key/values.

It is used by the class ITM.show_values(gui=True).
"""
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QApplication, QTreeView, QVBoxLayout

class GUI_values(QWidget):

    def __init__(self, data):
        QWidget.__init__(self)
        self.treeView = QTreeView()
        self.model = QStandardItemModel()
        self.addItems(self.model, data)
        self.treeView.setModel(self.model)
        layout = QVBoxLayout()
        layout.addWidget(self.treeView)
        self.setLayout(layout)

    def addItems(self, parent, elements):
        for k in sorted(elements.keys()):
            item = QStandardItem(k)
            parent.appendRow(item)
            if type(elements[k]) == dict:
                self.addItems(item, elements[k])
            else:
                child = QStandardItem(str(elements[k]))
                item.appendRow(child)


def show_values(data):
    app = QApplication([])
    G = GUI_values(data)
    G.show()
    app.exec_()
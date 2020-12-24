# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/ListWidgets/TrialListWidget.py
# Compiled at: 2020-04-29 16:54:29
# Size of source mod 2**32: 1800 bytes
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtCore
import os

class TrialListWidget(QWidget):

    def __init__(self):
        self.trial_paths = []
        self.trial_items = []
        super().__init__()
        self.list = QListWidget()
        self.setStyleSheet('QListView::item { border-bottom: 1px solid rgb(50, 65, 75); }')
        self.top_labels_layout = QHBoxLayout()
        label1 = QLabel(text='Trial Selection')
        self.top_labels_layout.addWidget(label1)
        label1.setStyleSheet('font-size:20')
        self.setMinimumHeight(100)
        self.model = QStandardItemModel(self.list)
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.top_labels_layout)
        self.layout.addWidget(self.list)
        self.roi_item_list = []
        self.setLayout(self.layout)

    def setItems(self, path):
        """
        Takes in a  path to a folder or a single file and adds the trials to the list view
        Parameters
        ----------
        path path to folder or single tiff file

        Returns
        -------
        Nothing
        """
        self.list.clear()
        self.trial_items = []
        if os.path.isfile(path):
            self.trial_paths = [
             path]
        else:
            self.trial_paths = sorted(os.listdir(path))
        for path in self.trial_paths:
            self.trial_items.append(QListWidgetItem(path, self.list))
            self.trial_items[(-1)].setFlags(self.trial_items[(-1)].flags() | QtCore.Qt.ItemIsUserCheckable)
            self.trial_items[(-1)].setCheckState(QtCore.Qt.Checked)

    def selectedTrials(self):
        return [self.trial_paths[x[0]] for x in enumerate(self.trial_items) if x[1].checkState() == Qt.CheckState.Checked]
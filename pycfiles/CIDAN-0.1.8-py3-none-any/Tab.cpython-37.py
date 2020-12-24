# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Tabs/Tab.py
# Compiled at: 2020-04-29 16:25:24
# Size of source mod 2**32: 1615 bytes
from typing import List
from CIDAN.GUI.ListWidgets.ROIListModule import *

class Column(QWidget):
    pass


class Tab(QWidget):

    def __init__(self, name, column_1, column_2, column_2_display=True):
        super().__init__()
        self.name = name
        self.column_1 = column_1
        self.column_2 = column_2
        self.setMinimumHeight(500)
        self.layout = QHBoxLayout()
        self.column_1_widget = Column()
        self.column_1_layout = QVBoxLayout()
        self.column_1_widget.setLayout(self.column_1_layout)
        self.column_1_widget.setStyleSheet('Column { border:1px solid rgb(50, 65, 75);} ')
        for module in column_1:
            self.column_1_layout.addWidget(module)

        self.layout.addWidget((self.column_1_widget), stretch=1)
        if column_2_display:
            self.column_2_layout = QVBoxLayout()
            self.column_2_widget = Column()
            self.column_2_widget.setStyleSheet('Column { border:1px solid rgb(50, 65, 75);} ')
            self.column_2_widget.setLayout(self.column_2_layout)
            for module in column_2:
                self.column_2_layout.addWidget(module)

            self.layout.addWidget((self.column_2_widget), stretch=1)
        self.setLayout(self.layout)


class AnalysisTab(Tab):

    def __init__(self, main_widget):
        super().__init__('Analysis', column_1=[], column_2=[])
# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plover_cat/__init__.py
# Compiled at: 2017-11-15 06:20:32
# Size of source mod 2**32: 747 bytes
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout
from plover.gui_qt.tool import Tool
from plover_cat.plover_cat_ui import Ui_PloverCAT
from plover_cat.main_window import PloverCATWindow

class PloverCAT(Tool):
    TITLE = 'PloverCAT'
    ROLE = 'plover_cat'
    ICON = ':/plover_cat/icon.svg'

    def __init__(self, engine):
        super().__init__(engine)
        self.setWindowFlags(Qt.Window | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.layout = QHBoxLayout()
        self.layout.addWidget(PloverCATWindow(engine))
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.finished.connect(lambda : None)
# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Data_Interaction/Thread.py
# Compiled at: 2020-04-29 15:51:33
# Size of source mod 2**32: 390 bytes
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from CIDAN.GUI.Data_Interaction.Signals import *

class Thread(QThread):

    def __init__(self, data_handler, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.signal = MatrixSignal()
        self.data_handler = data_handler

    def run(self):
        pass
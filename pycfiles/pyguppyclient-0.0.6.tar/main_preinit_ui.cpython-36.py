# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\source\main_preinit_ui.py
# Compiled at: 2019-04-14 12:51:37
# Size of source mod 2**32: 570 bytes
__doc__ = '\ninit UI class.\n'
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
try:
    from Ui_main import Ui_MainWindow
except ImportError as e:
    print('--1 --', e)
    try:
        from .Ui_main import Ui_MainWindow
    except ImportError as e:
        print('--2 --', e)

from Tools.BasePara import *

class Ui_initUI(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _initUI(self):
        """initUI"""
        pass
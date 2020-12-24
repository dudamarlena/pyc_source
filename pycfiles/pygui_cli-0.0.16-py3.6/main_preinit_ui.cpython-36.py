# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\source\main_preinit_ui.py
# Compiled at: 2019-04-14 12:51:37
# Size of source mod 2**32: 570 bytes
"""
init UI class.
"""
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
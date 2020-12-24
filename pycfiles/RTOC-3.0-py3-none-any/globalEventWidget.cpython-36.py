# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\RTOC_GUI\globalEventWidget.py
# Compiled at: 2019-04-23 10:37:58
# Size of source mod 2**32: 708 bytes
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import uic
import os, sys, logging as log
log.basicConfig(level=(log.INFO))
logging = log.getLogger(__name__)

class GlobalEventWidget(QtWidgets.QWidget):
    refresh = QtCore.pyqtSignal()

    def __init__(self, logger):
        super(GlobalEventWidget, self).__init__()
        if getattr(sys, 'frozen', False):
            packagedir = os.path.dirname(sys.executable) + '/RTOC/RTOC_GUI'
        else:
            packagedir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(packagedir + '/ui/globalEventWidget.ui', self)
        self.logger = logger
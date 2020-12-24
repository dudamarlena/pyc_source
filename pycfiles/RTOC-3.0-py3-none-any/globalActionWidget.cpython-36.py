# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\RTOC_GUI\globalActionWidget.py
# Compiled at: 2019-04-23 10:37:58
# Size of source mod 2**32: 711 bytes
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import uic
import os, sys, logging as log
log.basicConfig(level=(log.INFO))
logging = log.getLogger(__name__)

class GlobalActionWidget(QtWidgets.QWidget):
    refresh = QtCore.pyqtSignal()

    def __init__(self, logger):
        super(GlobalActionWidget, self).__init__()
        if getattr(sys, 'frozen', False):
            packagedir = os.path.dirname(sys.executable) + '/RTOC/RTOC_GUI'
        else:
            packagedir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(packagedir + '/ui/globalActionWidget.ui', self)
        self.logger = logger
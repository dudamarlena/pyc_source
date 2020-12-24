# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thejoeejoee/projects/VUT-FIT-IFJ-2017-tests/ifj2017/ide/core/core.py
# Compiled at: 2017-11-08 17:12:51
# Size of source mod 2**32: 403 bytes
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtGui import QGuiApplication

class Core(QObject):

    @pyqtSlot(float, result=float)
    def scaledSize(self, ref_size: float) -> float:
        if ref_size == 0.0:
            return 0.0
        dpi = QGuiApplication.primaryScreen().logicalDotsPerInch()
        ref_dpi = 96
        return ref_size * (dpi / ref_dpi)
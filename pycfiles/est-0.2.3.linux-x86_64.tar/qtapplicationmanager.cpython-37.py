# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/gui/qtapplicationmanager.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 2073 bytes
"""
This module is used to manage the rsync between files for transfert.
"""
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '26/06/2019'
from AnyQt.QtWidgets import QApplication
from AnyQt.QtCore import Qt, QUrl, QEvent, pyqtSignal as Signal
from est.core.utils.designpattern import singleton

@singleton
class QApplicationManager(QApplication):
    __doc__ = 'Return a singleton on the CanvasApplication'
    fileOpenRequest = Signal(QUrl)

    def __init__(self):
        QApplication.__init__(self, [])
        self.setAttribute(Qt.AA_DontShowIconsInMenus, True)

    def event(self, event):
        if event.type() == QEvent.FileOpen:
            self.fileOpenRequest.emit(event.url())
        return QApplication.event(self, event)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/qtapplicationmanager.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 2012 bytes
"""
This module is used to manage the rsync between files for transfert.
"""
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '11/04/2017'
from silx.gui import qt
from tomwer.core.utils.Singleton import singleton

@singleton
class QApplicationManager(qt.QApplication):
    __doc__ = 'Return a singleton on the CanvasApplication'
    fileOpenRequest = qt.Signal(qt.QUrl)

    def __init__(self):
        qt.QApplication.__init__(self, [])
        self.setAttribute(qt.Qt.AA_DontShowIconsInMenus, True)

    def event(self, event):
        if event.type() == qt.QEvent.FileOpen:
            self.fileOpenRequest.emit(event.url())
        return qt.QApplication.event(self, event)
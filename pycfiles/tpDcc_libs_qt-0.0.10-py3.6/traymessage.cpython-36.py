# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/core/traymessage.py
# Compiled at: 2020-04-26 16:40:12
# Size of source mod 2**32: 944 bytes
"""
Module that contains custom tray balloon
"""
from __future__ import print_function, division, absolute_import
from Qt.QtWidgets import *

class TrayMessage(QWidget, object):

    def __init__(self, parent=None):
        super(TrayMessage, self).__init__(parent=parent)
        self._tools_icon = None
        self.tray_icon_menu = QMenu(self)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setToolTip('Tray')
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        if not QSystemTrayIcon.isSystemTrayAvailable():
            raise OSError('Tray Icon is not available!')
        self.tray_icon.show()

    def show_message(self, title, msg):
        try:
            self.tray_icon.showMessage(title, msg, self._tools_icon)
        except Exception:
            self.tray_icon.showMessage(title, msg)
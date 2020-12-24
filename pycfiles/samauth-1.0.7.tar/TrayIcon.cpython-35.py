# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/samer/Seafile/Source/Source/Authenticator/SamAuthenticator/TrayIcon.py
# Compiled at: 2018-03-25 18:56:02
# Size of source mod 2**32: 737 bytes
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, qApp
from PyQt5.Qt import QIcon
import os

class SamAuthenticatorTrayIcon(QSystemTrayIcon):
    IconTooltip_normal = 'Sam Authenticator'

    def __init__(self, main_win, icon, parent=None):
        QSystemTrayIcon.__init__(self, parent)
        self.setIcon(icon)
        self.main_win = main_win
        self.menu = QMenu(parent)
        self.show_action = self.menu.addAction('Show')
        self.menu.addSeparator()
        self.exit_action = self.menu.addAction('Exit')
        self.setContextMenu(self.menu)
        self.exit_action.triggered.connect(qApp.quit)
        self.show_action.triggered.connect(self.main_win.raise_)
        self.setToolTip(self.IconTooltip_normal)
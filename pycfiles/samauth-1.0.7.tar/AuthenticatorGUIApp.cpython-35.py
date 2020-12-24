# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/samer/Seafile/Source/Source/Authenticator/SamAuthenticator/AuthenticatorGUIApp.py
# Compiled at: 2018-03-27 16:03:34
# Size of source mod 2**32: 235 bytes
from PyQt5.QtWidgets import QApplication
import SamAuthenticator.AuthenticatorWindow as MainWindow, sys

def start():
    app = QApplication(sys.argv)
    w = MainWindow.AuthenticatorGUI()
    w.show()
    return app.exec_()
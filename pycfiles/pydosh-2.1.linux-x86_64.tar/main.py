# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pydosh/main.py
# Compiled at: 2014-02-11 15:09:41
import sys
from PySide import QtGui, QtCore
from dialogs import LoginDialog
from mainWindow import PydoshWindow
import stylesheet, pydosh_rc

def main():
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(':/icons/pydosh.png'))
    QtCore.QCoreApplication.setApplicationName('pydosh')
    QtCore.QCoreApplication.setOrganizationName('innerhippy')
    QtCore.QCoreApplication.setOrganizationDomain('innerhippy.com')
    menubar = QtGui.QMenuBar()
    stylesheet.setStylesheet()
    loginDialog = LoginDialog()
    loginDialog.show()
    loginDialog.raise_()
    if loginDialog.exec_():
        window = PydoshWindow()
        window.show()
        return app.exec_()
    return -1


if __name__ == '__main__':
    sys.exit(main())
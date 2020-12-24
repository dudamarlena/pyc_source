# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
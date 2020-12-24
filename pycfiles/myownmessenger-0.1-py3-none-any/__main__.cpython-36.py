# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmitry.kovalenko/MyOwnMess/my_own_messenger/__main__.py
# Compiled at: 2018-01-17 11:22:57
# Size of source mod 2**32: 1033 bytes
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QThread, pyqtSlot
import subprocess, sys, my_own_messenger.login_page as login_page

def main():
    ui.pushButton.clicked.connect(authentification)
    login_window.show()
    sys.exit(appl.exec_())


def authentification():
    login = ui.LoginPlainTextEdit.toPlainText()
    password = ui.PasswordPlainTextEdit.toPlainText()
    print(login, password)
    subprocess.Popen(('python3.6 -m my_own_messenger/client_gui localhost 7777 {}'.format(login)), shell=True)
    exit(0)
    return (login, password)


if __name__ == '__main__':
    appl = QtWidgets.QApplication(sys.argv)
    login_window = QtWidgets.QMainWindow()
    ui = login_page.Ui_MainWindow()
    ui.setupUi(login_window)
    main()
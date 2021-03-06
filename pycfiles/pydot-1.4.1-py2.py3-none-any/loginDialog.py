# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pydosh/dialogs/loginDialog.py
# Compiled at: 2014-02-11 15:09:41
from PySide import QtCore, QtGui
from pydosh.ui_login import Ui_Login
from pydosh import utils
from pydosh.database import db, DatabaseNotInitialisedException, ConnectionException

class LoginDialog(Ui_Login, QtGui.QDialog):

    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent=parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.connectionButton.clicked.connect(self.activateConnection)
        self.closeButton.clicked.connect(self.reject)
        self.hostnameEdit.setText(db.hostname)
        self.databaseEdit.setText(db.database)
        self.usernameEdit.setText(db.username)
        self.passwordEdit.setText(db.password)
        self.portSpinBox.setValue(db.port)

    def activateConnection(self):
        db.database = self.databaseEdit.text()
        db.hostname = self.hostnameEdit.text()
        db.username = self.usernameEdit.text()
        db.password = self.passwordEdit.text()
        db.port = self.portSpinBox.value()
        try:
            with utils.showWaitCursor():
                db.connect()
        except DatabaseNotInitialisedException:
            if QtGui.QMessageBox.question(self, 'Database', 'Database %s is empty, do you want to initialise it?' % db.database, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
                try:
                    db.initialise()
                except ConnectionException as err:
                    QtGui.QMessageBox.critical(self, 'Database ', str(err))
                else:
                    QtGui.QMessageBox.information(self, 'Database', 'Database initialised successfully')

            else:
                return
        except ConnectionException as err:
            QtGui.QMessageBox.warning(self, 'Database', 'Failed to connect: %s' % str(err))
        else:
            self.accept()
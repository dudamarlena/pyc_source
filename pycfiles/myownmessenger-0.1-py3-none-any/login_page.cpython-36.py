# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmitry.kovalenko/MyOwnMess/my_own_messenger/login_page.py
# Compiled at: 2018-01-18 12:51:49
# Size of source mod 2**32: 3228 bytes
import os
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(646, 528)
        MainWindow.setStyleSheet('\nQPushButton {\n    background-color: #39424f;\n    border: 1px solid #39424f;\n    border-radius: 4px;\n    color: #fafafa;\n    padding: 8px 24px;\n\n}\nQPushButton:hover {\n    background-color: #BBC7DA;\n}\nQPushButton:focus {\n    outline: none;\n    border: 1px solid #8699B5;\n    text-decoration: underline;\n}\nQPushButton:pressed {\n    background-color: #8699B5;\n}\n')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 20, 371, 191))
        self.label.setText('')
        parent_dir_name = os.path.dirname(os.path.realpath(__file__)) + '/'
        self.label.setPixmap(QtGui.QPixmap('{}MyOwn.png'.format(parent_dir_name)))
        self.label.setObjectName('label')
        self.PasswordPlainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.PasswordPlainTextEdit.setGeometry(QtCore.QRect(180, 327, 311, 71))
        self.PasswordPlainTextEdit.setObjectName('PasswordPlainTextEdit')
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 190, 161, 31))
        self.label_2.setObjectName('label_2')
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(180, 300, 68, 17))
        self.label_3.setObjectName('label_3')
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(240, 420, 201, 51))
        self.pushButton.setObjectName('pushButton')
        self.LoginPlainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.LoginPlainTextEdit.setGeometry(QtCore.QRect(180, 220, 311, 78))
        self.LoginPlainTextEdit.setObjectName('LoginPlainTextEdit')
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 646, 25))
        self.menubar.setObjectName('menubar')
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName('statusbar')
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'MainWindow'))
        self.label_2.setText(_translate('MainWindow', 'Login'))
        self.label_3.setText(_translate('MainWindow', 'Password'))
        self.pushButton.setText(_translate('MainWindow', "Let's Chat!"))
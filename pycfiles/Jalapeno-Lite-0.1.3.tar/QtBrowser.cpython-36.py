# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jakob/Jest/Jalapeno/GUI/Gutils/QtBrowser.py
# Compiled at: 2017-03-21 10:25:52
# Size of source mod 2**32: 934 bytes
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.setWindowTitle('My Browser')
        self.setWindowIcon(QIcon('icons/penguin.png'))
        self.show()
        self.browser = QWebEngineView()
        url = 'https://127.0.0.1:5588'
        self.browser.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)


def Browse(listener):
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
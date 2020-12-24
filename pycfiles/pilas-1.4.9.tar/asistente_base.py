# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/asistente/asistente_base.py
# Compiled at: 2016-12-23 13:26:53
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)


except AttributeError:

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_AsistenteWindow(object):

    def setupUi(self, AsistenteWindow):
        AsistenteWindow.setObjectName(_fromUtf8('AsistenteWindow'))
        AsistenteWindow.resize(615, 480)
        AsistenteWindow.setMinimumSize(QtCore.QSize(615, 480))
        AsistenteWindow.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8('../../../pilas/pilas/data/pilas.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AsistenteWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(AsistenteWindow)
        self.centralwidget.setAcceptDrops(False)
        self.centralwidget.setObjectName(_fromUtf8('centralwidget'))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8('gridLayout'))
        self.webView = QtWebKit.QWebView(self.centralwidget)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8('about:blank')))
        self.webView.setObjectName(_fromUtf8('webView'))
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)
        AsistenteWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(AsistenteWindow)
        self.statusbar.setObjectName(_fromUtf8('statusbar'))
        AsistenteWindow.setStatusBar(self.statusbar)
        self.salir_action = QtGui.QAction(AsistenteWindow)
        self.salir_action.setObjectName(_fromUtf8('salir_action'))
        self.retranslateUi(AsistenteWindow)
        QtCore.QMetaObject.connectSlotsByName(AsistenteWindow)

    def retranslateUi(self, AsistenteWindow):
        AsistenteWindow.setWindowTitle(_translate('AsistenteWindow', 'pilas-engine', None))
        self.salir_action.setText(_translate('AsistenteWindow', 'Salir', None))
        return


from PyQt4 import QtWebKit
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    AsistenteWindow = QtGui.QMainWindow()
    ui = Ui_AsistenteWindow()
    ui.setupUi(AsistenteWindow)
    AsistenteWindow.show()
    sys.exit(app.exec_())
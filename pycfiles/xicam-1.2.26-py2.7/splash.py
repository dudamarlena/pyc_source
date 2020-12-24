# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicamlauncher\splash.py
# Compiled at: 2018-08-27 17:21:07
from PySide import QtCore, QtGui

class SplashScreen(QtGui.QSplashScreen):

    def __init__(self, pixmap, f=None):
        super(SplashScreen, self).__init__(pixmap, f)
        self.pixmap = pixmap
        self.timer = QtCore.QTimer(self)
        self.timer.singleShot(1000, self.launchwindow)
        self.timer.singleShot(3000, self.hide)
        self._launching = False

    def mousePressEvent(self, *args, **kwargs):
        self.timer.stop()
        self.launchwindow()

    def launchwindow(self):
        if not self._launching:
            self._launching = True
            import xicam
            from xicam import xglobals
            app = QtGui.QApplication.instance()
            xglobals.window = xicam.xicamwindow.MyMainWindow(app)
            self.timer.stop()
            xglobals.window.ui.show()
            xglobals.window.ui.raise_()
            xglobals.window.ui.activateWindow()
            app.setActiveWindow(xglobals.window.ui)
            self.hide()
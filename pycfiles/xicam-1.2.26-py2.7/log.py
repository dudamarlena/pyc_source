# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\log.py
# Compiled at: 2018-08-27 17:21:07
import base
from PySide import QtGui, QtCore
from xicam import xglobals
from pipeline import msg
import numpy as np
colors = {msg.DEBUG: QtCore.Qt.gray, msg.ERROR: QtCore.Qt.darkRed, msg.CRITICAL: QtCore.Qt.red, msg.INFO: QtCore.Qt.white, 
   msg.WARNING: QtCore.Qt.yellow}

class LogPlugin(base.plugin):
    name = 'Log'
    sigLog = QtCore.Signal(int, str, str, np.ndarray)

    def __init__(self, *args, **kwargs):
        self.centerwidget = QtGui.QListWidget()
        self.rightwidget = None
        self.featureform = None
        self.bottomwidget = None
        self.leftwidget = None
        self.toolbar = None
        msg.guilogcallable = self.log
        msg.flushbacklog()
        super(LogPlugin, self).__init__(*args, **kwargs)
        return

    def log(self, level, timestamp, s, image=None, icon=None):
        item = QtGui.QListWidgetItem(s)
        item.setForeground(QtGui.QBrush(colors[level]))
        item.setToolTip(timestamp)
        self.centerwidget.addItem(item)
        if image is not None:
            image = np.uint8((image - image.min()) / image.ptp() * 255.0)
            pixmap = QtGui.QPixmap.fromImage(QtGui.QImage(image, image.shape[0], image.shape[1], QtGui.QImage.Format_Indexed8))
            i = QtGui.QListWidgetItem()
            w = QtGui.QLabel()
            w.setPixmap(pixmap)
            size = QtCore.QSize(*image.shape)
            w.setFixedSize(size)
            i.setSizeHint(w.sizeHint())
            self.centerwidget.addItem(i)
            self.centerwidget.setItemWidget(i, w)
        return

    def openSelected(self, *args, **kwargs):
        xglobals.plugins['Timeline'].instance.activate()
        xglobals.plugins['Timeline'].instance.openSelected(*args, **kwargs)

    def openfiles(self, *args, **kwargs):
        xglobals.plugins['Viewer'].instance.activate()
        xglobals.plugins['Viewer'].instance.openfiles(*args, **kwargs)

    def calibrate(self):
        xglobals.plugins['Viewer'].instance.activate()
        xglobals.plugins['Viewer'].instance.calibrate()

    def currentImage(self):
        xglobals.plugins['Viewer'].instance.activate()
        xglobals.plugins['Viewer'].instance.currentImage()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\MOTD.py
# Compiled at: 2018-08-27 17:21:07
import base
from PySide import QtGui
import os
from xicam import xglobals
import widgets

class MOTDPlugin(base.plugin):
    name = 'MOTD'
    hidden = True

    def __init__(self, *args, **kwargs):
        self.rightwidget = None
        try:
            from PySide import QtWebKit
        except ImportError:
            pass
        else:
            self.centerwidget = webview = QtWebKit.QWebView()
            webview.load('MOTD.html')

        super(MOTDPlugin, self).__init__(*args, **kwargs)
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
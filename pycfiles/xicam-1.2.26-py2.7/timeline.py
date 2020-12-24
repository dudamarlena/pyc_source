# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\timeline.py
# Compiled at: 2019-03-07 15:21:12
import platform
from pipeline import msg
op_sys = platform.system()
if op_sys == 'Darwin':
    try:
        from Foundation import NSURL
    except ImportError:
        msg.logMessage('NSURL not found. Drag and drop may not work correctly', msg.WARNING)

import base, viewer
from PySide import QtGui, QtCore
import os, numpy as np, widgets
from pipeline import calibration
from xicam.widgets.NDTimelinePlotWidget import TimelinePlot
from collections import OrderedDict

class TimelinePlugin(base.plugin):
    name = 'Timeline'
    sigUpdateExperiment = viewer.ViewerPlugin.sigUpdateExperiment

    def __init__(self, *args, **kwargs):
        self.centerwidget = QtGui.QTabWidget()
        self.centerwidget.currentChanged.connect(self.currentChanged)
        self.centerwidget.setDocumentMode(True)
        self.centerwidget.setTabsClosable(True)
        self.centerwidget.tabCloseRequested.connect(self.tabCloseRequested)
        self.bottomwidget = TimelinePlot()
        self.rightmodes = viewer.rightmodes
        self.toolbar = widgets.toolbar.difftoolbar()
        self.toolbar.connecttriggers(self.calibrate, self.centerfind, self.refinecenter, self.redrawcurrent, self.redrawcurrent, self.remeshmode, self.linecut, self.vertcut, self.horzcut, self.redrawcurrent, self.redrawcurrent, self.redrawcurrent, self.roi, self.arccut, self.polymask, process=self.process)
        super(TimelinePlugin, self).__init__(*args, **kwargs)
        self.centerwidget.setAcceptDrops(True)
        self.centerwidget.dragEnterEvent = self.dragEnterEvent
        self.centerwidget.dropEvent = self.dropEvent

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        if op_sys == 'Darwin':
            fnames = [ str(NSURL.URLWithString_(str(url.toString())).filePathURL().path()) for url in e.mimeData().urls() ]
        else:
            fnames = e.mimeData().urls()
        e.accept()
        self.openfiles(fnames)

    def tabCloseRequested(self, index):
        self.centerwidget.widget(index).deleteLater()

    def getCurrentTab(self):
        return self.centerwidget.currentWidget().widget

    def currentImage(self):
        return self.getCurrentTab()

    def calibrate(self, algorithm=calibration.fourierAutocorrelation, calibrant='AgBh'):
        self.getCurrentTab().calibrate(algorithm, calibrant)

    def centerfind(self):
        self.getCurrentTab().centerfind()

    def refinecenter(self):
        self.getCurrentTab().refinecenter()

    def redrawcurrent(self):
        self.getCurrentTab().redrawimage()

    def remeshmode(self):
        self.getCurrentTab().redrawimage()
        self.getCurrentTab().replot()

    def linecut(self):
        self.getCurrentTab().linecut()

    def vertcut(self):
        self.getCurrentTab().verticalcut()

    def horzcut(self):
        self.getCurrentTab().horizontalcut()

    def roi(self):
        self.getCurrentTab().roi()

    def arccut(self):
        self.getCurrentTab().arccut()

    def polymask(self):
        self.getCurrentTab().polymask()

    def process(self):
        self.getCurrentTab().processtimeline()

    def makeVideo(self):
        pass

    def currentChanged(self, index):
        for tab in [ self.centerwidget.widget(i) for i in range(self.centerwidget.count()) ]:
            tab.unload()

        self.centerwidget.currentWidget().load()

    @QtCore.Slot(object, object)
    def unpack(self, *args):
        if isinstance(args[1], OrderedDict):
            self.bottomwidget.addData(args[0], **args[1])
        elif isinstance(args[1], tuple):
            self.bottomwidget.addData(args[0], *args[1])
        else:
            self.bottomwidget.addData(args[0], args[1])

    def openfiles(self, files, operation=None, operationname=None):
        self.activate()
        widget = widgets.OOMTabItem(itemclass=widgets.timelineViewer, files=files, toolbar=self.toolbar)
        self.centerwidget.addTab(widget, 'Timeline: ' + os.path.basename(files[0]) + ', ...')
        self.centerwidget.setCurrentWidget(widget)
        self.getCurrentTab().sigAddTimelineData.connect(self.unpack)
        self.getCurrentTab().sigClearTimeline.connect(self.bottomwidget.clear)


def convertto8bit(image):
    image *= (np.iinfo(np.uint8).max - 1) / float(np.max(image))
    return image.astype(np.uint8).copy()
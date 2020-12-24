# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/ui/pyqt_houdini.py
# Compiled at: 2012-09-24 08:25:08
"""
This module helps you use PyQt in Houdini's GUI by integrating PyQt's event
loop into Houdini's.  Replace calls to QApplication.exec_() in your
code with calls to pyqt_houdini.exec_(app).
"""
import hou
from PyQt4 import QtCore
from PyQt4 import QtGui

class IntegratedEventLoop(object):
    """This class behaves like QEventLoop except it allows PyQt to run inside
    Houdini's event loop on the main thread.  You probably just want to
    call exec_() below instead of using this class directly.
    """

    def __init__(self, application, dialogs):
        self.application = application
        self.dialogs = dialogs
        self.event_loop = QtCore.QEventLoop()

    def exec_(self):
        hou.ui.addEventLoopCallback(self.processEvents)

    def processEvents(self):
        if not anyQtWindowsAreOpen():
            hou.ui.removeEventLoopCallback(self.processEvents)
        self.event_loop.processEvents()
        self.application.sendPostedEvents(None, 0)
        return


def anyQtWindowsAreOpen():
    return any(w.isVisible() for w in QtGui.QApplication.topLevelWidgets())


def exec_(application, *args):
    """You cannot call QApplication.exec_, or Houdini will freeze while PyQt
    waits for and processes events.  Instead, call this function to allow
    Houdini's and PyQt's event loops to coexist.  Pass in any dialogs as
    extra arguments, if you want to ensure that something holds a reference
    to them while the event loop runs.

    This function returns right away.
    """
    IntegratedEventLoop(application, args).exec_()


def execSynchronously(application, *args):
    """This function is like exec_, except it will not return until all PyQt
    windows have closed.  Houdini will remain responsive while the PyQt window
    is open.
    """
    exec_(application, *args)
    hou.ui.waitUntil(lambda : not anyQtWindowsAreOpen())
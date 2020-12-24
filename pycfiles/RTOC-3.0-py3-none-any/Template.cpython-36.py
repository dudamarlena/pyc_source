# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\Template.py
# Compiled at: 2019-05-26 22:40:01
# Size of source mod 2**32: 4320 bytes
"""
This template shows, how to implement plugins in RTOC

RTOC version 2.0

A plugin needs to import RTOC.LoggerPlugin to be recognized by RTOC.
"""
try:
    from LoggerPlugin import LoggerPlugin
except ImportError:
    from RTOC.LoggerPlugin import LoggerPlugin

import sys, time
from PyQt5 import uic
from PyQt5 import QtWidgets
import numpy as np
DEVICENAME = 'Template'
AUTORUN = True
SAMPLERATE = 1

class Plugin(LoggerPlugin):

    def __init__(self, stream=None, plot=None, event=None):
        super(Plugin, self).__init__(stream, plot, event)
        self.setDeviceName(DEVICENAME)
        self.smallGUI = True
        self._firstrun = True
        self.setPerpetualTimer((self._updateT), samplerate=SAMPLERATE)
        if AUTORUN:
            self.start()

    def _updateT(self):
        """
        This function is called periodically after calling ``self.start()``.

        This example will generate a sinus and a cosinus curve. And send them to RTOC.

        """
        y1 = np.sin(time.time())
        y2 = np.cos(time.time())
        self.stream([y1, y2], snames=['Sinus', 'Cosinus'], unit=['kg', 'm'])
        self.plot([-10, 0], [2, 1], sname='Plot', unit='Wow')
        if self._firstrun:
            self.event('Test event', sname='Plot', id='testID')
            self._firstrun = False

    def loadGUI(self):
        """
        This function is used to initialize the Plugin-GUI, which will be available in :doc:`GUI`.

        This is optional.

        Returns:
            PyQt5.QWidget: A widget containing optional plugin-GUI
        """
        self.widget = QtWidgets.QWidget()
        packagedir = self.getDir(__file__)
        uic.loadUi(packagedir + '/Template/template.ui', self.widget)
        return self.widget


hasGUI = True
if __name__ == '__main__':
    if hasGUI:
        app = QtWidgets.QApplication(sys.argv)
        myapp = QtWidgets.QMainWindow()
    widget = Plugin()
    if hasGUI:
        widget.loadGUI()
        myapp.setCentralWidget(widget.widget)
        myapp.show()
        app.exec_()
    widget.run = False
    sys.exit()
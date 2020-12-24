# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\gui\settings\venvs.py
# Compiled at: 2018-05-17 15:54:06
# Size of source mod 2**32: 657 bytes
from qtpy.QtGui import *
from qtpy.QtWidgets import *
from xicam.gui.static import path
from xicam.plugins import SettingsPlugin

class VenvsSettingsPlugin(SettingsPlugin):
    name = 'Virtual Environments'

    def __init__(self):
        self.widget = QLabel('test')
        super(VenvsSettingsPlugin, self).__init__(QIcon(str(path('icons/python.png'))), self.name, self.widget)

    def save(self):
        pass

    def restore(self, state):
        pass
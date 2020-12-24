# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\gui\settings\appearance.py
# Compiled at: 2018-05-17 15:54:06
# Size of source mod 2**32: 2297 bytes
from collections import OrderedDict
import qdarkstyle
from qtmodern import styles
from qtpy.QtGui import *
from qtpy.QtWidgets import QApplication
from xicam.gui.static import path
import pyqtgraph as pg
from xicam import plugins
from xicam.plugins import SettingsPlugin

def setDefault():
    QApplication.instance().setStyleSheet('')


def setDark():
    QApplication.instance().setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


def setModern():
    styles.dark(QApplication.instance())


def setUglyGreen():
    QApplication.instance().setStyleSheet('QWidget {background-color: darkgreen;}')


def setPlotWhite():
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')


def setPlotDefault():
    pass


if plugins.qt_is_safe:
    AppearanceSettingsPlugin = SettingsPlugin.fromParameter(QIcon(str(path('icons/colors.png'))), 'Appearance', [
     dict(name='Theme', values=(OrderedDict([('Default', setDefault),
      (
       'QDarkStyle', setDark),
      (
       'QtModern', setModern),
      (
       'UglyGreen', setUglyGreen)])),
       type='list'),
     dict(name='Plot Theme (requires restart)', values=(OrderedDict([('Default (Dark)', setPlotDefault),
      (
       'Publication (White)',
       setPlotWhite)])),
       type='list')])

    def apply(self):
        self.parameter['Theme']()
        self.parameter['Plot Theme (requires restart)']()


    AppearanceSettingsPlugin.apply = apply
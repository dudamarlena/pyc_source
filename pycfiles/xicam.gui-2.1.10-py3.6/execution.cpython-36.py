# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\gui\settings\execution.py
# Compiled at: 2018-07-06 18:13:03
# Size of source mod 2**32: 1742 bytes
from collections import OrderedDict
import qdarkstyle
from qtmodern import styles
from qtpy.QtGui import *
from qtpy.QtWidgets import QApplication
from xicam.gui.static import path
import pyqtgraph as pg
from xicam import plugins
from xicam.core.execution import localexecutor, daskexecutor, camlinkexecutor
from xicam.core import execution
from xicam.plugins import SettingsPlugin
if plugins.qt_is_safe:
    AppearanceSettingsPlugin = SettingsPlugin.fromParameter(QIcon(str(path('icons/cpu.png'))), 'Execution', [
     dict(name='Executor', values=(OrderedDict([
      ('Local Threaded',
       localexecutor.LocalExecutor()),
      (
       'Local Service',
       daskexecutor.DaskExecutor()),
      ('Cam-link', None)])),
       value='Local Threaded',
       type='list')])
    execution.executor = AppearanceSettingsPlugin.parameter['Executor']

    def apply(self):
        execution.executor = self.parameter['Executor']


    AppearanceSettingsPlugin.apply = apply
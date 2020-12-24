# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_device_monitor/windows/base.py
# Compiled at: 2020-04-09 04:27:42
# Size of source mod 2**32: 1192 bytes
"""Utility base classes for Qt widgets."""
from qtpy import QtWidgets, uic
from os import path

class BaseWindow(QtWidgets.QMainWindow):
    __doc__ = 'Base class for Qt MainWindow widgets. Automatically creates a MainWindow widget based on the supplied UI file,\n    and assigns all child widgets as attributes to itself.'

    def __init__(self, ui_file, *args, **kwargs):
        (super(BaseWindow, self).__init__)(*args, **kwargs)
        uic.loadUi(path.join(path.dirname(__file__), '..', 'res', 'ui', ui_file), self)
        for child in self.findChildren(QtWidgets.QWidget):
            name = child.objectName()
            setattr(self, name, child)


class BaseWidget(QtWidgets.QWidget):
    __doc__ = 'Base class for generic Qt widgets. Automatically creates a Qt widget based on the supplied UI file,\n    and assigns all child widgets as attributes to itself.'

    def __init__(self, ui_file, *args, **kwargs):
        (super(BaseWidget, self).__init__)(*args, **kwargs)
        uic.loadUi(path.join(path.dirname(__file__), '..', 'res', 'ui', ui_file), self)
        for child in self.findChildren(QtWidgets.QWidget):
            name = child.objectName()
            setattr(self, name, child)
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/abstract_widget.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui, QtCore

class AbstractSearchWidget(QtGui.QWidget):
    expand_search_options_signal = QtCore.pyqtSignal()
    cancel_signal = QtCore.pyqtSignal()
    search_signal = QtCore.pyqtSignal(str)
    on_arrow_down_signal = QtCore.pyqtSignal()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/abstract_widget.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui, QtCore

class AbstractSearchWidget(QtGui.QWidget):
    expand_search_options_signal = QtCore.pyqtSignal()
    cancel_signal = QtCore.pyqtSignal()
    search_signal = QtCore.pyqtSignal(str)
    on_arrow_down_signal = QtCore.pyqtSignal()
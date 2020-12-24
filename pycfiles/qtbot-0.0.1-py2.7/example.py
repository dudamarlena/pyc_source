# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/example.py
# Compiled at: 2015-03-18 10:50:15
from PyQt4 import QtGui
import qtbot
app = QtGui.QApplication([])
dlg = QtGui.QFileDialog()
fname = '/foo/bar'
qtbot.handle_modal_widget(fname, wait=False)
dlg.exec_()
assert fname == dlg.selectedFiles()[0]
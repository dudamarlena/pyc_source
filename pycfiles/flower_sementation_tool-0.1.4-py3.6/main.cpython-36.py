# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/segtool/main.py
# Compiled at: 2019-05-29 04:38:41
# Size of source mod 2**32: 358 bytes
import sys
from PyQt5 import QtWidgets
from gui.app import DesignerMainWindow
app = QtWidgets.QApplication(sys.argv)
dmw = DesignerMainWindow()
dmw.show()
sys.exit(app.exec_())
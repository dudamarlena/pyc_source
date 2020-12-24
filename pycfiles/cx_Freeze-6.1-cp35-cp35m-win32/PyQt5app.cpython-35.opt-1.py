# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\samples\PyQt5\PyQt5app.py
# Compiled at: 2019-08-29 22:24:38
# Size of source mod 2**32: 215 bytes
import sys
from PyQt5.QtWidgets import QApplication, QWidget
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Simple')
window.show()
app.exec_()
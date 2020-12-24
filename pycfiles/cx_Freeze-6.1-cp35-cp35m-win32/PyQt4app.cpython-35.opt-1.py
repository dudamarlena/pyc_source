# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\samples\PyQt4\PyQt4app.py
# Compiled at: 2019-08-29 22:24:38
# Size of source mod 2**32: 175 bytes
import sys
from PyQt4.QtGui import QApplication, QDialog
app = QApplication(sys.argv)
form = QDialog()
form.show()
app.exec_()
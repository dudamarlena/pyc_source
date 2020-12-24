# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyinstruments\pyhardwaredb\run.py
# Compiled at: 2013-10-09 11:09:05
from guidata import qapplication as __qapplication
from pyinstruments.pyhardwaredb import gui
gui()
_APP = __qapplication()
_APP.exec_()
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyinstruments\pyhardwaredb\run.py
# Compiled at: 2013-10-09 11:09:05
from guidata import qapplication as __qapplication
from pyinstruments.pyhardwaredb import gui
gui()
_APP = __qapplication()
_APP.exec_()
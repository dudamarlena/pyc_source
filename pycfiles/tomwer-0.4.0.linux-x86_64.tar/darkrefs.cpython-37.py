# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/synctools/darkrefs.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 2025 bytes
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '09/01/2018'
from silx.gui import qt
from tomwer.core.process.reconstruction.darkref.darkrefs import DarkRefsWorker
from tomwer.core.process.reconstruction.darkref.darkrefscopy import DarkRefsCopyWorker

class DarkRefsWorkerThread(DarkRefsWorker, qt.QThread):
    __doc__ = 'Implementation of the DarkRefsWorker on a qt.QThread for gui'

    def __init__(self):
        DarkRefsWorker.__init__(self)
        qt.QThread.__init__(self)


class DarkRefsCopyWorkerThread(DarkRefsCopyWorker, qt.QThread):
    __doc__ = 'Implementation of the DarkRefsCopyWorker on a qt.QThread for gui'

    def __init__(self):
        DarkRefsCopyWorker.__init__(self)
        qt.QThread.__init__(self)
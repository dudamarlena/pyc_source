# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/synctools/datatransfert.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 1667 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '28/01/2019'
from silx.gui import qt
import tomwer.core.process.datatransfert as FolderTransfertP

class FolderTransfert(FolderTransfertP, qt.QObject):
    scanready = qt.Signal(str)

    def __init__(self):
        FolderTransfertP.__init__(self)
        qt.QObject.__init__(self)
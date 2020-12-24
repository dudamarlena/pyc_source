# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/utils/waiterthread.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 1842 bytes
"""
This module is used to manage observations. Initially on files.
Observations are runned on a thread and run each n seconds.
They are manage by thread and signals
"""
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '09/02/2017'
from silx.gui import qt
import time

class QWaiterThread(qt.QThread):
    __doc__ = 'simple thread wich wait for waitingTime to be finished'

    def __init__(self, waitingTime):
        qt.QThread.__init__(self)
        self.waitingTime = waitingTime

    def run(self):
        time.sleep(self.waitingTime)
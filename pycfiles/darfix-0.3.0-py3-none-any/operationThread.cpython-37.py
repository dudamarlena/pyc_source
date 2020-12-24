# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/garrigaf/Documents/git/darfix/build/lib/darfix/gui/operationThread.py
# Compiled at: 2019-11-28 10:44:40
# Size of source mod 2**32: 1892 bytes
__authors__ = [
 'J. Garriga']
__license__ = 'MIT'
__date__ = '26/07/2019'
from silx.gui import qt

class OperationThread(qt.QThread):
    __doc__ = '\n    Given a function and a set of arguments, it calls it whenever the thread\n    is started.\n    '

    def __init__(self, function):
        qt.QThread.__init__(self)
        self.func = function
        self.args = []

    def setArgs(self, *args):
        """
        Function to set the arguments of the function

        :param List args:
        """
        self.args = args

    def run(self):
        self.data = (self.func)(*self.args)
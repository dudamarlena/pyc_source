# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/taurusoperation.py
# Compiled at: 2019-08-19 15:09:29
"""This module contains the base taurus operation classes"""
__all__ = [
 'TaurusOperation', 'WriteAttrOperation']
__docformat__ = 'restructuredtext'
from .util.log import Logger

class TaurusOperation(Logger):

    def __init__(self, name='TaurusOperation', parent=None, callbacks=None):
        self.call__init__(Logger, name, parent)
        if callbacks is None:
            callbacks = []
        self._callbacks = callbacks
        self._dangerMessage = None
        self._isDangerous = False
        return

    def getDevice(self):
        pass

    def setCallbacks(self, callbacks):
        self._callbacks = callbacks

    def getCallbacks(self):
        return self._callbacks

    def execute(self):
        for f in self._callbacks:
            f(operation=self)

    def isDangerous(self):
        return self._isDangerous

    def setDangerMessage(self, dangerMessage=None):
        """if dangerMessage is None, the operation is considered safe"""
        self._dangerMessage = dangerMessage
        self._isDangerous = dangerMessage is not None
        return

    def getDangerMessage(self):
        return self._dangerMessage

    def resetDangerMessage(self):
        self.setDangerMessage(None)
        return


class WriteAttrOperation(TaurusOperation):

    def __init__(self, attr, value, callbacks=None):
        self.call__init__(TaurusOperation, 'WriteAttrOperation', attr, callbacks=callbacks)
        self.attr = attr
        self.value = value

    def execute(self):
        self.attr.write(self.value)
        TaurusOperation.execute(self)
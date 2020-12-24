# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\srllib\testing\qtgui\mock.py
# Compiled at: 2012-05-11 12:09:02
from PyQt4.QtCore import QObject
from srllib.testing.mock import *

class QMock(QObject, Mock):
    """ Mock class that also inherits from QObject.
    """
    __connections = {}

    def __init__(self, *args, **kwds):
        QObject.__init__(self)
        Mock.__init__(self, *args, **kwds)

    @classmethod
    def mock_clear_connections(cls):
        cls.__connections.clear()

    def mock_is_connected(self, slot, signal):
        return slot in self.__connections.setdefault(self, {}).setdefault(signal, [])

    @classmethod
    def connect(cls, emitter, signal, slot):
        cls.__connections.setdefault(emitter, {}).setdefault(signal, []).append(slot)

    def emit(self, signal, *args):
        """ Allow signal emission.
        """
        for slot in self.__connections.setdefault(self, {}).setdefault(signal, []):
            slot(*args)


class QWidgetMock(QMock):

    def __init__(self, *args, **kwds):
        QMock.__init__(self, *args, **kwds)
        self.__enabled = True

    def setEnabled(self, enabled):
        self.__enabled = enabled

    def isEnabled(self):
        return self.__enabled


class QDialogMock(QWidgetMock):
    pass
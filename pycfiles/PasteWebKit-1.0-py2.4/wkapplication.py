# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/wkapplication.py
# Compiled at: 2006-10-22 17:01:02
"""
A mostly dummy class to simulate the Webware Application object.
"""
from wkcommon import NoDefault
import threading
try:
    from TaskKit.Scheduler import Scheduler
except ImportError:
    Scheduler = None

_taskManager = None
_makeTaskManagerLock = threading.Lock()

def taskManager():
    global _taskManager
    if _taskManager is None:
        if Scheduler is None:
            assert 0, 'FakeWebware is not installed, and/or TaskKit is not available'
        _makeTaskManagerLock.acquire()
        try:
            if _taskManager is None:
                _taskManager = Scheduler(1)
                _taskManager.start()
        finally:
            _makeTaskManagerLock.release()
    return _taskManager


class Application(object):
    __module__ = __name__

    def __init__(self, transaction):
        self._transaction = transaction

    def forward(self, trans, url, context=None):
        assert context is None, 'Contexts are not supported'
        trans.forward(url)
        return

    def setting(self, setting, default=NoDefault):
        assert default is not NoDefault, 'No settings are defined'
        return default

    def taskManager(self):
        return taskManager()
# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/reporting/reporter_proxy.py
# Compiled at: 2009-10-07 18:08:46
"""The proxy used as a result object for PyUnit suites"""
from test_info import create_test_info
from err_info import create_err_info

def synchronize(func, lock=None):
    if lock is None:
        import threading
        lock = threading.RLock()

    def wrapper(*args, **kwargs):
        lock.acquire()
        try:
            return func(*args, **kwargs)
        finally:
            lock.release()

    return wrapper
    return


class ReporterProxy:
    __module__ = __name__

    def __init__(self, threads=False):
        self.observing_reporters = []
        if threads:
            self._apply_method = synchronize(self._apply_method)

    def add_observer(self, reporter):
        self.observing_reporters.append(reporter)

    def _apply_method(self, name, *args, **kwargs):
        for reporter in self.observing_reporters:
            getattr(reporter, name)(*args, **kwargs)

    def setParameters(self, **parameters):
        self._apply_method('setParameters', **parameters)

    def start(self):
        self._apply_method('start')

    def done(self):
        self._apply_method('done')

    def startTest(self, test):
        self._apply_method('startTest', create_test_info(test))

    def stopTest(self, test):
        self._apply_method('stopTest', create_test_info(test))

    def addError(self, test, err):
        test_info = create_test_info(test)
        err_info = create_err_info(test, err)
        if err_info.is_skip():
            self._apply_method('addSkip', test_info, err_info)
            return
        self._apply_method('addError', test_info, err_info)

    def addFailure(self, test, err):
        self._apply_method('addFailure', create_test_info(test), create_err_info(test, err))

    def addSuccess(self, test):
        self._apply_method('addSuccess', create_test_info(test))

    def addAssert(self, test, assertName, varList, exception):
        self._apply_method('addAssert', create_test_info(test), assertName, varList, exception)

    def addSkip(self, test, err, isRegistered=True):
        self._apply_method('addSkip', create_test_info(test), create_err_info(test, err), isRegistered)

    def isSuccessful(self):
        for reporter in self.observing_reporters:
            if not reporter.isSuccessful():
                return False

        return True

    def isFailed(self):
        for reporter in self.observing_reporters:
            if hasattr(reporter, 'isFailed'):
                if reporter.isFailed():
                    return True
            elif not reporter.isSuccessful():
                return True

        return False
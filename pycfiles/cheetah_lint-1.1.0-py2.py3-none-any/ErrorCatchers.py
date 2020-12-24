# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/ErrorCatchers.py
# Compiled at: 2019-09-22 10:12:27
import time
from Cheetah.NameMapper import NotFound

class Error(Exception):
    pass


class ErrorCatcher:
    _exceptionsToCatch = (
     NotFound,)

    def __init__(self, templateObj):
        pass

    def exceptions(self):
        return self._exceptionsToCatch

    def warn(self, exc_val, code, rawCode, lineCol):
        return rawCode


Echo = ErrorCatcher

class BigEcho(ErrorCatcher):

    def warn(self, exc_val, code, rawCode, lineCol):
        return '===============&lt;' + rawCode + ' could not be found&gt;' + '==============='


class KeyError(ErrorCatcher):

    def warn(self, exc_val, code, rawCode, lineCol):
        raise KeyError("no '%s' in this Template Object's Search List" % rawCode)


class ListErrors(ErrorCatcher):
    """Accumulate a list of errors."""
    _timeFormat = '%c'

    def __init__(self, templateObj):
        ErrorCatcher.__init__(self, templateObj)
        self._errors = []

    def warn(self, exc_val, code, rawCode, lineCol):
        dict = locals().copy()
        del dict['self']
        dict['time'] = time.strftime(self._timeFormat, time.localtime(time.time()))
        self._errors.append(dict)
        return rawCode

    def listErrors(self):
        """Return the list of errors."""
        return self._errors
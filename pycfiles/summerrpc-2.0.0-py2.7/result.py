# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/result.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'Result']
__authors__ = ['Tim Chow']

class Result(object):

    def __init__(self):
        self._result = None
        self._exc = None
        self._meta = None
        return

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result):
        self._result = result

    @property
    def exc(self):
        return self._exc

    @exc.setter
    def exc(self, exc):
        self._exc = exc

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self, meta):
        self._meta = meta
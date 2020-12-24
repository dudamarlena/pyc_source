# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/field.py
# Compiled at: 2018-05-30 05:31:20
__all__ = [
 'AutoWiredField', 'ValueField']
__authors__ = ['Tim Chow']

class AutoWiredField(object):

    def __init__(self, auto_wired=None):
        self._auto_wired = auto_wired

    @property
    def auto_wired(self):
        return self._auto_wired


class ValueField(object):

    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
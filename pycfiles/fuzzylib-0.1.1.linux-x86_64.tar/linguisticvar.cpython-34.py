# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/fuzzylib/linguisticvar.py
# Compiled at: 2015-09-29 17:24:14
# Size of source mod 2**32: 642 bytes
from collections import OrderedDict

class LinguisticVar:

    def __init__(self, name, minval=-10, maxval=10):
        self._name = name
        self._minval = minval
        self._maxval = maxval
        self._sets = OrderedDict()

    def get_name(self):
        return self._name

    def add_set(self, name, function):
        self._sets[name] = function

    def get_set(self, name):
        return self._sets[name]

    def get_range(self):
        return (
         self._minval, self._maxval)

    def set_range(self, minval, maxval):
        self._minval = minval
        self._maxval = maxval
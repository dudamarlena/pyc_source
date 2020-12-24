# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aiogcd/orm/properties/integervalue.py
# Compiled at: 2019-09-11 07:21:09
# Size of source mod 2**32: 625 bytes
"""integervalue.py

Created on: May 19, 2017
    Author: Jeroen van der Heijden <jeroen@transceptor.technology>
"""
from .value import Value

class IntegerValue(Value):

    def check_value(self, value):
        if not isinstance(value, int):
            raise TypeError("Expecting an value of type 'int' for property {!r} but received type {!r}.".format(self.name, value.__class__.__name__))

    def set_value(self, model, value):
        self.check_value(value)
        super().set_value(model, int(value))
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aiogcd/orm/properties/keyvalue.py
# Compiled at: 2019-09-11 07:21:09
# Size of source mod 2**32: 645 bytes
"""keyvalue.py

Created on: May 19, 2017
    Author: Jeroen van der Heijden <jeroen@transceptor.technology>
"""
from connector.key import Key
from .value import Value

class KeyValue(Value):

    def check_value(self, value):
        if not isinstance(value, Key):
            raise TypeError("Expecting an value of type 'Key' for property {!r} but received type {!r}.".format(self.name, value.__class__.__name__))

    def set_value(self, model, value):
        self.check_value(value)
        super().set_value(model, value)
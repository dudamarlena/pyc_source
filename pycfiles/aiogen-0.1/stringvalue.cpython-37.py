# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aiogcd/orm/properties/stringvalue.py
# Compiled at: 2019-09-11 07:21:09
# Size of source mod 2**32: 558 bytes
__doc__ = 'stringvalue.py\n\nCreated on: May 19, 2017\n    Author: Jeroen van der Heijden <jeroen@transceptor.technology>\n'
from .value import Value

class StringValue(Value):

    def check_value(self, value):
        if not isinstance(value, str):
            raise TypeError("Expecting an value of type 'str' for property {!r} but received type {!r}.".format(self.name, value.__class__.__name__))

    def set_value(self, model, value):
        self.check_value(value)
        super().set_value(model, value)
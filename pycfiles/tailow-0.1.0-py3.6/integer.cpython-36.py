# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tailow/fields/integer.py
# Compiled at: 2018-06-14 12:05:35
# Size of source mod 2**32: 787 bytes
from tailow.fields.base import BaseField

class IntegerField(BaseField):

    def __init__(self, min_value=None, max_value=None, **kwargs):
        (super(IntegerField, self).__init__)(**kwargs)
        self.min_value = min_value
        self.max_value = max_value

    def _to_int(self, value):
        if value:
            return int(value)
        else:
            return int(self.default)

    def from_son(self, value):
        return self._to_int(value)

    def to_son(self, value):
        return self._to_int(value)

    def to_query(self, value):
        return self._to_int(value)

    def validate(self, value):
        val = self._to_int(value)
        if val < self.min_value:
            return False
        else:
            if val > self.max_value:
                return False
            return True
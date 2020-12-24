# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tailow/fields/string.py
# Compiled at: 2018-06-26 04:52:04
# Size of source mod 2**32: 904 bytes
import re
from tailow.fields.base import BaseField

class StringField(BaseField):

    def __init__(self, max_length=None, **kwargs):
        (super(StringField, self).__init__)(**kwargs)
        self.max_length = max_length

    def from_son(self, value):
        return str(value)

    def to_son(self, value):
        return str(value)

    def validate(self, value):
        return isinstance(value, str) and len(value) <= self.max_length


class TextField(StringField):

    def validate(self, value):
        return isinstance(value, str)


class RegexField(StringField):

    def __init__(self, pattern=None, **kwargs):
        (super(RegexField, self).__init__)(**kwargs)
        self.pattern = re.compile(pattern) if pattern else None

    def validate(self, value):
        if self.pattern:
            m = self.pattern.match(value)
            if m:
                return True
            return False
        else:
            return True
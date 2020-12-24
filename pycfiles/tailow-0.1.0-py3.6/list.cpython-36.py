# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tailow/fields/list.py
# Compiled at: 2018-06-14 12:05:35
# Size of source mod 2**32: 492 bytes
from tailow.fields.base import BaseField

class ListField(BaseField):

    def __init__(self, sub_field=None, **kwargs):
        (super(ListField, self).__init__)(**kwargs)
        if not sub_field:
            raise ValueError('ListField subtype not mentioned')
        self.sub_field = sub_field

    def from_son(self, value):
        return map(lambda x: self.sub_field.from_son(x), value)

    def to_son(self, value):
        return map(lambda x: self.sub_field.to_son(x), value)
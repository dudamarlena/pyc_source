# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tailow/fields/reference.py
# Compiled at: 2018-06-14 12:05:35
# Size of source mod 2**32: 825 bytes
""" reference field """
from bson.objectid import ObjectId
from .base import BaseField

class ReferenceField(BaseField):
    __doc__ = ' Reference field property '

    def __init__(self, kls, *args, **kwargs):
        self.kls = kls
        self._is_reference = True
        (super(ReferenceField, self).__init__)(*args, **kwargs)

    def validate(self, value):
        """ validate if it is a valid field """
        from tailow.document import Document
        if isinstance(value, (self.kls, Document)):
            return True
        else:
            return False

    def to_son(self, value):
        if value is None:
            return
        else:
            if isinstance(value, ObjectId):
                return value
            if hasattr(value, '_id'):
                return value._id
            return value.id

    def from_son(self, value):
        return value
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/oid.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 1116 bytes
from __future__ import unicode_literals
from bson import ObjectId as OID
from collections import MutableMapping
from datetime import datetime, timedelta
from .base import Field
from ....schema import Attribute
from ....schema.compat import unicode

class ObjectId(Field):
    __foreign__ = 'objectId'
    __disallowed_operators__ = {'#array'}
    default = Attribute()

    def __fixup__(self, document):
        super(ObjectId, self).__fixup__(document)
        try:
            self.default
        except AttributeError:
            if self.__name__ == '_id':
                self.default = lambda : OID()

    def to_foreign(self, obj, name, value):
        if isinstance(value, OID):
            return value
        else:
            if isinstance(value, datetime):
                return OID.from_datetime(value)
            else:
                if isinstance(value, timedelta):
                    return OID.from_datetime(datetime.utcnow() + value)
                if isinstance(value, MutableMapping):
                    if '_id' in value:
                        return OID(value['_id'])
            return OID(unicode(value))
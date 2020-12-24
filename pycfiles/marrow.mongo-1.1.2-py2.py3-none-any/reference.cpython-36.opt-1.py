# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/reference.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 3191 bytes
from __future__ import unicode_literals
from collections import Mapping
from bson import ObjectId as OID
from bson import DBRef
from bson.errors import InvalidId
from .. import Document, Field
from ....package.canonical import name as canon
from ....package.loader import traverse
from ....schema import Attribute
from ....schema.compat import odict, str, unicode
from .base import _HasKind, Field

class Reference(_HasKind, Field):
    concrete = Attribute(default=False)
    cache = Attribute(default=None)

    @property
    def __foreign__(self):
        """Advertise that we store a simple reference, or deep reference, or object, depending on configuration."""
        if self.cache:
            return 'object'
        else:
            if self.concrete:
                return 'dbPointer'
            return 'objectId'

    def _populate_cache(self, value):
        inst = odict()
        if isinstance(value, Document):
            try:
                inst['_id'] = value.__data__['_id']
                if getattr(value, '__type_store__', None):
                    inst[value.__type_store__] = canon(value.__class__)
            except KeyError:
                raise ValueError('Must reference a document with an _id.')

        elif isinstance(value, Mapping):
            try:
                inst['_id'] = value['_id']
            except KeyError:
                raise ValueError('Must reference a document with an _id.')

        else:
            if isinstance(value, OID):
                inst['_id'] = value
            elif isinstance(value, (str, unicode)):
                if len(value) == 24:
                    try:
                        inst['_id'] = OID(value)
                    except InvalidId:
                        raise ValueError('Not referenceable: ' + repr(value))

            else:
                raise ValueError('Not referenceable: ' + repr(value))
            for field in self.cache:
                if any(chunk.isnumeric() for chunk in field.split('.')):
                    raise ValueError('May not contain numeric array references.')
                try:
                    nested = traverse(value, field)
                except LookupError:
                    pass
                else:
                    current = inst
                    parts = field.split('.')
                    for part in parts[:-1]:
                        current = current.setdefault(part, odict())

                    current[parts[(-1)]] = nested

            return inst

    def to_foreign(self, obj, name, value):
        """Transform to a MongoDB-safe value."""
        if self.cache:
            return self._populate_cache(value)
        else:
            identifier = value
            if isinstance(value, Document):
                identifier = value.__data__.get('_id', None)
                if identifier is None:
                    raise ValueError('Can only store a reference to a saved Document instance with an `_id` stored.')
            else:
                if isinstance(value, (str, unicode)):
                    if len(value) == 24:
                        try:
                            identifier = OID(value)
                        except InvalidId:
                            pass

            kind = self._kind(obj.__class__)
            if self.concrete:
                if isinstance(value, Document):
                    if value.__collection__:
                        return DBRef(value.__collection__, identifier)
                if getattr(kind, '__collection__', None):
                    return DBRef(kind.__collection__, identifier)
                raise ValueError('Could not infer collection name.')
            return identifier
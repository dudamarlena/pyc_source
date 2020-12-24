# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/django-hstore/django_hstore/descriptors.py
# Compiled at: 2015-06-28 18:07:27
# Size of source mod 2**32: 1283 bytes
from django.db import models
from .dict import HStoreDict, HStoreReferenceDict
__all__ = [
 'HStoreDescriptor',
 'HStoreReferenceDescriptor',
 'SerializedDictDescriptor']

class HStoreDescriptor(models.fields.subclassing.Creator):
    _DictClass = HStoreDict

    def __init__(self, *args, **kwargs):
        self.schema_mode = kwargs.pop('schema_mode', False)
        super(HStoreDescriptor, self).__init__(*args, **kwargs)

    def __set__(self, obj, value):
        value = self.field.to_python(value)
        if isinstance(value, dict):
            value = self._DictClass(value=value, field=self.field, instance=obj, schema_mode=self.schema_mode)
        obj.__dict__[self.field.name] = value


class SerializedDictDescriptor(models.fields.subclassing.Creator):
    _DictClass = dict

    def __set__(self, obj, value):
        if value:
            if self.field._from_db(obj):
                value = self.field.to_python(value)
        obj.__dict__[self.field.name] = value


class HStoreReferenceDescriptor(HStoreDescriptor):
    _DictClass = HStoreReferenceDict
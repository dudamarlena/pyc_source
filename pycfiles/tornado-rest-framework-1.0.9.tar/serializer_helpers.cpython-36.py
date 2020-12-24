# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/70/_7dmwj6x12q099dhb0z0p7p80000gn/T/pycharm-packaging/djangorestframework/rest_framework/utils/serializer_helpers.py
# Compiled at: 2018-05-14 04:48:23
# Size of source mod 2**32: 5187 bytes
from __future__ import unicode_literals
import collections
from collections import OrderedDict
from django.utils.encoding import force_text
from rest_framework.compat import unicode_to_repr
from rest_framework.utils import json

class ReturnDict(OrderedDict):
    __doc__ = '\n    Return object from `serializer.data` for the `Serializer` class.\n    Includes a backlink to the serializer instance for renderers\n    to use if they need richer field information.\n    '

    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop('serializer')
        (super(ReturnDict, self).__init__)(*args, **kwargs)

    def copy(self):
        return ReturnDict(self, serializer=(self.serializer))

    def __repr__(self):
        return dict.__repr__(self)

    def __reduce__(self):
        return (
         dict, (dict(self),))


class ReturnList(list):
    __doc__ = '\n    Return object from `serializer.data` for the `SerializerList` class.\n    Includes a backlink to the serializer instance for renderers\n    to use if they need richer field information.\n    '

    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop('serializer')
        (super(ReturnList, self).__init__)(*args, **kwargs)

    def __repr__(self):
        return list.__repr__(self)

    def __reduce__(self):
        return (
         list, (list(self),))


class BoundField(object):
    __doc__ = '\n    A field object that also includes `.value` and `.error` properties.\n    Returned when iterating over a serializer instance,\n    providing an API similar to Django forms and form fields.\n    '

    def __init__(self, field, value, errors, prefix=''):
        self._field = field
        self._prefix = prefix
        self.value = value
        self.errors = errors
        self.name = prefix + self.field_name

    def __getattr__(self, attr_name):
        return getattr(self._field, attr_name)

    @property
    def _proxy_class(self):
        return self._field.__class__

    def __repr__(self):
        return unicode_to_repr('<%s value=%s errors=%s>' % (
         self.__class__.__name__, self.value, self.errors))

    def as_form_field(self):
        value = '' if self.value is None or self.value is False else self.value
        return self.__class__(self._field, value, self.errors, self._prefix)


class JSONBoundField(BoundField):

    def as_form_field(self):
        value = self.value
        if not getattr(value, 'is_json_string', False):
            try:
                value = json.dumps((self.value), sort_keys=True, indent=4)
            except (TypeError, ValueError):
                pass

        return self.__class__(self._field, value, self.errors, self._prefix)


class NestedBoundField(BoundField):
    __doc__ = '\n    This `BoundField` additionally implements __iter__ and __getitem__\n    in order to support nested bound fields. This class is the type of\n    `BoundField` that is used for serializer fields.\n    '

    def __init__(self, field, value, errors, prefix=''):
        if value is None or value is '':
            value = {}
        super(NestedBoundField, self).__init__(field, value, errors, prefix)

    def __iter__(self):
        for field in self.fields.values():
            yield self[field.field_name]

    def __getitem__(self, key):
        field = self.fields[key]
        value = self.value.get(key) if self.value else None
        error = self.errors.get(key) if isinstance(self.errors, dict) else None
        if hasattr(field, 'fields'):
            return NestedBoundField(field, value, error, prefix=(self.name + '.'))
        else:
            return BoundField(field, value, error, prefix=(self.name + '.'))

    def as_form_field(self):
        values = {}
        for key, value in self.value.items():
            if isinstance(value, (list, dict)):
                values[key] = value
            else:
                values[key] = '' if value is None or value is False else force_text(value)

        return self.__class__(self._field, values, self.errors, self._prefix)


class BindingDict(collections.MutableMapping):
    __doc__ = '\n    This dict-like object is used to store fields on a serializer.\n\n    This ensures that whenever fields are added to the serializer we call\n    `field.bind()` so that the `field_name` and `parent` attributes\n    can be set correctly.\n    '

    def __init__(self, serializer):
        self.serializer = serializer
        self.fields = OrderedDict()

    def __setitem__(self, key, field):
        self.fields[key] = field
        field.bind(field_name=key, parent=(self.serializer))

    def __getitem__(self, key):
        return self.fields[key]

    def __delitem__(self, key):
        del self.fields[key]

    def __iter__(self):
        return iter(self.fields)

    def __len__(self):
        return len(self.fields)

    def __repr__(self):
        return dict.__repr__(self.fields)
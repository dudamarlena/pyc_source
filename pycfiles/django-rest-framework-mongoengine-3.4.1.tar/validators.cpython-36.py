# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: W:\Projects\django-rest-framework-mongoengine\rest_framework_mongoengine\validators.py
# Compiled at: 2020-01-02 08:16:18
# Size of source mod 2**32: 3710 bytes
from __future__ import unicode_literals
from rest_framework import validators
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField
from rest_framework_mongoengine.repr import smart_repr

class MongoValidatorMixin:

    def exclude_current_instance(self, queryset, instance):
        if instance is not None:
            return queryset.filter(pk__ne=(instance.pk))
        else:
            return queryset


class UniqueValidator(MongoValidatorMixin, validators.UniqueValidator):
    __doc__ = ' Replacement of DRF UniqueValidator.\n\n    Used by :class:`DocumentSerializer` for fields, present in unique indexes.\n    '

    def __init__(self, queryset, message=None, lookup=''):
        """
        Setting empty string as default lookup for UniqueValidator.
        For Mongoengine exact is a shortcut to query with regular experission.
        This fixes https://github.com/umutbozkurt/django-rest-framework-mongoengine/issues/264
        """
        super(UniqueValidator, self).__init__(queryset, message, lookup)

    def __call__(self, value, serializer_field):
        field_name = serializer_field.source_attrs[(-1)]
        instance = getattr(serializer_field.parent, 'instance', None)
        queryset = self.queryset
        queryset = self.filter_queryset(value, queryset, field_name)
        queryset = self.exclude_current_instance(queryset, instance)
        if queryset.first():
            raise ValidationError(self.message.format())

    def __repr__(self):
        return '<%s(queryset=%s)>' % (
         self.__class__.__name__,
         smart_repr(self.queryset))


class UniqueTogetherValidator(MongoValidatorMixin, validators.UniqueTogetherValidator):
    __doc__ = ' Replacement of DRF UniqueTogetherValidator.\n\n    Used by :class:`DocumentSerializer` for fields, present in unique indexes.\n    '

    def __call__(self, attrs, serializer):
        try:
            self.enforce_required_fields(attrs, serializer)
        except SkipField:
            return
        else:
            instance = getattr(serializer, 'instance', None)
            queryset = self.queryset
            queryset = self.filter_queryset(attrs, queryset, serializer)
            queryset = self.exclude_current_instance(queryset, instance)
            checked_values = [value for field, value in attrs.items() if field in self.fields]
            if None not in checked_values:
                if queryset.first():
                    field_names = ', '.join(self.fields)
                    raise ValidationError(self.message.format(field_names=field_names))

    def __repr__(self):
        return '<%s(queryset=%s, fields=%s)>' % (
         self.__class__.__name__,
         smart_repr(self.queryset),
         smart_repr(self.fields))


class OptionalUniqueTogetherValidator(UniqueTogetherValidator):
    __doc__ = '\n    This validator passes validation if all of validation fields are missing. (for use with partial data)\n    '

    def enforce_required_fields(self, attrs, serializer):
        try:
            super(OptionalUniqueTogetherValidator, self).enforce_required_fields(attrs, serializer)
        except ValidationError as e:
            if set(e.detail.keys()) == set(self.fields):
                raise SkipField()
            else:
                raise
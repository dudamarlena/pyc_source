# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/django_enums/enum.py
# Compiled at: 2017-02-20 05:33:34
from __future__ import division, print_function, absolute_import, unicode_literals
from django import forms
from django.db import models
from django.utils.functional import curry
from enum import Enum as BaseEnum
from itertools import ifilter
from logging import getLogger
import django, six
logger = getLogger(__name__)

class Enum(BaseEnum):

    def __init__(self, key, label):
        self.key = key
        self.label = label

    @classmethod
    def get_by_key(cls, key):
        return next(iter(filter(lambda x: x.key == key, list(cls))), None)

    @classmethod
    def tuples(cls):
        return map(lambda x: x.value, list(cls))

    @classmethod
    def choices(cls):
        return cls.tuples()

    @classmethod
    def get_max_length(cls):
        return len(max(list(cls), key=lambda x: len(x.key)).key)

    def __str__(self):
        return self.label

    def __unicode__(self):
        return unicode(self.label)


class EnumField(models.CharField):

    def __init__(self, enum, *args, **kwargs):
        self.enum = enum
        self.default_enum = kwargs.pop(b'default', None)
        kwargs[b'max_length'] = self.enum.get_max_length()
        kwargs[b'choices'] = self.enum.choices()
        if isinstance(self.default_enum, self.enum):
            kwargs[b'default'] = self.default_enum.key
        super(EnumField, self).__init__(*args, **kwargs)
        return

    def check(self, **kwargs):
        logger.debug(b'call: check kwargs=%s' % kwargs)
        errors = super(EnumField, self).check(**kwargs)
        errors.extend(self._check_enum_attribute(**kwargs))
        errors.extend(self._check_default_attribute(**kwargs))
        return errors

    def _check_enum_attribute(self, **kwargs):
        logger.debug(b'call: _check_enum_attribute kwargs=%s' % kwargs)
        errors = super(EnumField, self).check(**kwargs)
        if self.enum is None:
            return [
             checks.Error(b"EnumFields must define a 'enum' attribute.", obj=self, id=b'django-enum.fields.E001')]
        else:
            return []
            return

    def _check_default_attribute(self, **kwargs):
        logger.debug(b'call: _check_default_attribute kwargs=%s' % kwargs)
        if self.default_enum is not None:
            if not isinstance(self.default_enum, self.enum):
                return [
                 checks.Error(b"'default' must be a member of %s." % self.enum.__name__, obj=self, id=b'django-enum.fields.E002')]
        return []

    @staticmethod
    def _get_display(self, field):
        return getattr(self, field.attname).label

    def contribute_to_class(self, cls, name, virtual_only=False):
        super(EnumField, self).contribute_to_class(cls, name, virtual_only)
        setattr(cls, b'get_%s_display' % self.name, curry(self._get_display, field=self))
        setattr(self.enum, b'__len__', lambda x: len(unicode(x)))

    def from_db_value(self, value, expression, connection, context):
        logger.debug(b'call: from_db_value value=%s%s' % (value, type(value)))
        return self.to_python(value)

    def to_python(self, value):
        """Returns an Enum object."""
        logger.debug(b'call: to_python value=%s%s' % (value, type(value)))
        if isinstance(value, Enum) or value is None:
            logger.debug(b'to_python returns %s%s' % (value, type(value)))
            return value
        else:
            ret = self.enum.get_by_key(value)
            logger.debug(b'to_python returns %s%s' % (ret, type(ret)))
            return ret

    def get_internal_type(self):
        logger.debug(b'call: get_internal_type')
        return b'EnumField'

    def db_type(self, connection):
        logger.debug(b'db_type returns char(%s)' % self.max_length)
        return b'char(%s)' % self.max_length

    def get_db_prep_lookup(self, lookup_type, value, connection, prepared=True):
        """Support 'exact' and 'in'."""
        logger.debug(b'call: get_db_prep_lookup lookup_type=%s, value=%s%s' % (lookup_type, value, type(value)))
        if lookup_type == b'exact':
            return [self.get_db_prep_value(value)]
        if lookup_type == b'in':
            return [ self.get_db_prep_value(v) for v in value ]
        raise TypeError(b'Lookup type %r not supported.' % lookup_type)

    def get_db_prep_value(self, value, connection, prapared=True, **kwargs):
        logger.debug(b'call: get_db_prep_value value=%s%s' % (value, type(value)))
        if isinstance(value, self.enum):
            return value.key
        if isinstance(value, basestring):
            return value
        raise Exception(b'%s is not a valid value.', value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def formfield(self, **kwargs):
        logger.debug(b'call: formfield kwargs=%s' % kwargs)
        defaults = {b'widget': forms.Select, 
           b'form_class': forms.ChoiceField, 
           b'choices': self.enum.choices()}
        defaults.update(kwargs)
        return super(EnumField, self).formfield(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super(EnumField, self).deconstruct()
        if django.VERSION >= (1, 9):
            kwargs[b'enum'] = self.enum
        else:
            path = b'django.db.models.fields.CharField'
        return (
         name, path, args, kwargs)
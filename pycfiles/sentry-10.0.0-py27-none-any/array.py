# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/db/models/fields/array.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import six
from django.conf import settings
from django.db import models
from sentry.utils import json
SOUTH = 'south' in settings.INSTALLED_APPS

class ArrayField(models.Field):

    def __init__(self, of=models.TextField, **kwargs):
        if isinstance(of, tuple) and SOUTH:
            from south.utils import ask_for_it_by_name as gf
            of = gf(of[0])(*of[1], **of[2])
        if isinstance(of, type):
            of = of()
        self.of = of
        kwargs['null'] = True
        super(ArrayField, self).__init__(**kwargs)

    def db_type(self, connection):
        engine = connection.settings_dict['ENGINE']
        if 'postgres' in engine:
            return ('{}[]').format(self.of.db_type(connection))
        return super(ArrayField, self).db_type(connection)

    def get_internal_type(self):
        return 'TextField'

    def to_python(self, value):
        if not value:
            value = []
        if isinstance(value, six.text_type):
            value = json.loads(value)
        return map(self.of.to_python, value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            engine = connection.settings_dict['ENGINE']
            if 'postgres' in engine:
                return value
            if value:
                return json.dumps(value)
            return None
        return value

    def get_prep_lookup(self, lookup_type, value):
        raise NotImplementedError(('{!r} lookup type for {!r} is not supported').format(lookup_type, self))

    def south_field_triple(self):
        from south.modelsinspector import introspector
        double = introspector(self.of)
        return (
         '%s.%s' % (self.__class__.__module__, self.__class__.__name__), [],
         {'of': (
                 ('{module}.{class_name}').format(module=self.of.__class__.__module__, class_name=self.of.__class__.__name__),
                 double[0],
                 double[1])})


if hasattr(models, 'SubfieldBase'):
    ArrayField = six.add_metaclass(models.SubfieldBase)(ArrayField)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/db/models/fields/uuid.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import importlib, six
from django.conf import settings
from django.db import models
from django.db.models.fields import NOT_PROVIDED
from psycopg2.extensions import register_adapter
from uuid import uuid4, UUID
SOUTH = 'south' in settings.INSTALLED_APPS

class UUIDField(models.Field):
    """Field for storing UUIDs."""
    description = 'Universally unique identifier.'

    def __init__(self, auto_add=False, coerce_to=UUID, **kwargs):
        """Instantiate the field."""
        if auto_add is True:
            auto_add = uuid4
        if isinstance(auto_add, six.text_type):
            module_name, member = auto_add.split(':')
            module = importlib.import_module(module_name)
            auto_add = getattr(module, member)
        self._auto_add = auto_add
        self._coerce_to = coerce_to
        if auto_add and 'editable' not in kwargs:
            kwargs['editable'] = False
        if kwargs.get('blank', False) and not kwargs.get('null', False):
            raise AttributeError((' ').join(('Blank UUIDs are stored as NULL. Therefore, setting',
                                             '`blank` to True requires `null` to be True.')))
        kwargs['max_length'] = 32
        super(UUIDField, self).__init__(**kwargs)

    def db_type(self, connection):
        engine = connection.settings_dict['ENGINE']
        if 'postgres' in engine:
            return 'uuid'
        return super(UUIDField, self).db_type(connection)

    def get_internal_type(self):
        return 'CharField'

    def get_prep_value(self, value):
        """Return a wrapped, valid UUID value."""
        if not value:
            if self.null or self._auto_add or self.default != NOT_PROVIDED:
                return None
            raise ValueError('Explicit UUID required unless either `null` is True or `auto_add` is given.')
        if isinstance(value, UUID):
            return value
        else:
            return UUID(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        """Return a UUID object. Also, ensure that psycopg2 is
        aware how to address that object.
        """
        engine = connection.settings_dict['ENGINE']
        if 'postgres' not in engine:
            if not prepared:
                value = self.get_prep_value(value)
            if value:
                return six.text_type(value.hex)
            return None
        return super(UUIDField, self).get_db_prep_value(value, connection, prepared=prepared)

    def pre_save(self, instance, add):
        """If auto is set, generate a UUID at random."""
        if self._auto_add and add and not getattr(instance, self.attname):
            uuid_value = self._auto_add()
            setattr(instance, self.attname, uuid_value)
            return uuid_value
        return super(UUIDField, self).pre_save(instance, add)

    def to_python(self, value):
        """Return a UUID object."""
        if isinstance(value, self._coerce_to) or not value:
            return value
        return self._coerce_to(value)

    @property
    def _auto_add_str(self):
        """Return a dot path, as a string, of the `_auto_add` callable.
        If `_auto_add` is a boolean, return it unchanged.
        """
        if isinstance(self._auto_add, bool):
            return self._auto_add
        return '%s:%s' % (self._auto_add.__module__, self._auto_add.__name__)


class UUIDAdapter(object):

    def __init__(self, value):
        if not isinstance(value, UUID):
            raise TypeError('UUIDAdapter only understands UUID objects.')
        self.value = value

    def getquoted(self):
        return ("'%s'" % self.value).encode('utf8')


if hasattr(models, 'SubfieldBase'):
    UUIDField = six.add_metaclass(models.SubfieldBase)(UUIDField)
register_adapter(UUID, UUIDAdapter)
if SOUTH:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([
     (
      (
       UUIDField,), [],
      {'auto_add': [
                    '_auto_add_str', {'default': False}], 
         'coerce_to': [
                     '_coerce_to', {'default': UUID}]})], ('^sentry\\.db\\.models\\.fields\\.uuid\\.UUIDField', ))
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/models/indexes.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import hashlib
from django.db.backends.utils import split_identifier
from django.utils.encoding import force_bytes
__all__ = [
 str(b'Index')]

class Index(object):
    suffix = b'idx'
    max_name_length = 30

    def __init__(self, fields=[], name=None):
        if not isinstance(fields, list):
            raise ValueError(b'Index.fields must be a list.')
        if not fields:
            raise ValueError(b'At least one field is required to define an index.')
        self.fields = fields
        self.fields_orders = [ (field_name[1:], b'DESC') if field_name.startswith(b'-') else (field_name, b'') for field_name in self.fields
                             ]
        self.name = name or b''
        if self.name:
            errors = self.check_name()
            if len(self.name) > self.max_name_length:
                errors.append(b'Index names cannot be longer than %s characters.' % self.max_name_length)
            if errors:
                raise ValueError(errors)

    def check_name(self):
        errors = []
        if self.name[0] == b'_':
            errors.append(b'Index names cannot start with an underscore (_).')
            self.name = b'D%s' % self.name[1:]
        elif self.name[0].isdigit():
            errors.append(b'Index names cannot start with a number (0-9).')
            self.name = b'D%s' % self.name[1:]
        return errors

    def get_sql_create_template_values(self, model, schema_editor, using):
        fields = [ model._meta.get_field(field_name) for field_name, order in self.fields_orders ]
        tablespace_sql = schema_editor._get_index_tablespace_sql(model, fields)
        quote_name = schema_editor.quote_name
        columns = [ (b'%s %s' % (quote_name(field.column), order)).strip() for field, (field_name, order) in zip(fields, self.fields_orders)
                  ]
        return {b'table': quote_name(model._meta.db_table), 
           b'name': quote_name(self.name), 
           b'columns': (b', ').join(columns), 
           b'using': using, 
           b'extra': tablespace_sql}

    def create_sql(self, model, schema_editor, using=b''):
        sql_create_index = schema_editor.sql_create_index
        sql_parameters = self.get_sql_create_template_values(model, schema_editor, using)
        return sql_create_index % sql_parameters

    def remove_sql(self, model, schema_editor):
        quote_name = schema_editor.quote_name
        return schema_editor.sql_delete_index % {b'table': quote_name(model._meta.db_table), 
           b'name': quote_name(self.name)}

    def deconstruct(self):
        path = b'%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        path = path.replace(b'django.db.models.indexes', b'django.db.models')
        return (path, (), {b'fields': self.fields, b'name': self.name})

    def clone(self):
        """Create a copy of this Index."""
        path, args, kwargs = self.deconstruct()
        return self.__class__(*args, **kwargs)

    @staticmethod
    def _hash_generator(*args):
        """
        Generate a 32-bit digest of a set of arguments that can be used to
        shorten identifying names.
        """
        h = hashlib.md5()
        for arg in args:
            h.update(force_bytes(arg))

        return h.hexdigest()[:6]

    def set_name_with_model(self, model):
        """
        Generate a unique name for the index.

        The name is divided into 3 parts - table name (12 chars), field name
        (8 chars) and unique hash + suffix (10 chars). Each part is made to
        fit its size by truncating the excess length.
        """
        _, table_name = split_identifier(model._meta.db_table)
        column_names = [ model._meta.get_field(field_name).column for field_name, order in self.fields_orders ]
        column_names_with_order = [ (b'-%s' if order else b'%s') % column_name for column_name, (field_name, order) in zip(column_names, self.fields_orders)
                                  ]
        hash_data = [
         table_name] + column_names_with_order + [self.suffix]
        self.name = b'%s_%s_%s' % (
         table_name[:11],
         column_names[0][:7],
         b'%s_%s' % (self._hash_generator(*hash_data), self.suffix))
        assert len(self.name) <= self.max_name_length, b'Index too long for multiple database support. Is self.suffix longer than 3 characters?'
        self.check_name()

    def __repr__(self):
        return b"<%s: fields='%s'>" % (self.__class__.__name__, (b', ').join(self.fields))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.deconstruct() == other.deconstruct()

    def __ne__(self, other):
        return not self == other
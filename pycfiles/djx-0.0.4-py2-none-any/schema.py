# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/backends/sqlite3/schema.py
# Compiled at: 2019-02-14 00:35:17
import codecs, contextlib, copy
from decimal import Decimal
from django.apps.registry import Apps
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.utils import six

class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    sql_delete_table = 'DROP TABLE %(table)s'
    sql_create_inline_fk = 'REFERENCES %(to_table)s (%(to_column)s)'
    sql_create_unique = 'CREATE UNIQUE INDEX %(name)s ON %(table)s (%(columns)s)'
    sql_delete_unique = 'DROP INDEX %(name)s'

    def __enter__(self):
        with self.connection.cursor() as (c):
            c.execute('PRAGMA foreign_keys')
            self._initial_pragma_fk = c.fetchone()[0]
            c.execute('PRAGMA foreign_keys = 0')
        return super(DatabaseSchemaEditor, self).__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        super(DatabaseSchemaEditor, self).__exit__(exc_type, exc_value, traceback)
        with self.connection.cursor() as (c):
            c.execute('PRAGMA foreign_keys = %s' % int(self._initial_pragma_fk))

    def quote_value(self, value):
        try:
            import sqlite3
            value = sqlite3.adapt(value)
        except ImportError:
            pass
        except sqlite3.ProgrammingError:
            pass

        if isinstance(value, type(True)):
            return str(int(value))
        else:
            if isinstance(value, (Decimal, float)):
                return str(value)
            if isinstance(value, six.integer_types):
                return str(value)
            if isinstance(value, six.string_types):
                return "'%s'" % six.text_type(value).replace("'", "''")
            if value is None:
                return 'NULL'
            if isinstance(value, (bytes, bytearray, six.memoryview)):
                value = bytes(value)
                hex_encoder = codecs.getencoder('hex_codec')
                value_hex, _length = hex_encoder(value)
                return "X'%s'" % value_hex.decode('ascii')
            raise ValueError('Cannot quote parameter value %r of type %s' % (value, type(value)))
            return

    def _remake_table(self, model, create_field=None, delete_field=None, alter_field=None):
        """
        Shortcut to transform a model from old_model into new_model

        The essential steps are:
          1. rename the model's existing table, e.g. "app_model" to "app_model__old"
          2. create a table with the updated definition called "app_model"
          3. copy the data from the old renamed table to the new table
          4. delete the "app_model__old" table
        """

        def is_self_referential(f):
            return f.is_relation and f.remote_field.model is model

        body = {f.name:(f.clone() if is_self_referential(f) else f) for f in model._meta.local_concrete_fields}
        mapping = {f.column:self.quote_name(f.column) for f in model._meta.local_concrete_fields}
        rename_mapping = {}
        restore_pk_field = None
        if getattr(create_field, 'primary_key', False) or alter_field and getattr(alter_field[1], 'primary_key', False):
            for name, field in list(body.items()):
                if field.primary_key:
                    field.primary_key = False
                    restore_pk_field = field
                    if field.auto_created:
                        del body[name]
                        del mapping[field.column]

        if create_field:
            body[create_field.name] = create_field
            if not create_field.many_to_many and create_field.concrete:
                mapping[create_field.column] = self.quote_value(self.effective_default(create_field))
        if alter_field:
            old_field, new_field = alter_field
            body.pop(old_field.name, None)
            mapping.pop(old_field.column, None)
            body[new_field.name] = new_field
            if old_field.null and not new_field.null:
                case_sql = 'coalesce(%(col)s, %(default)s)' % {'col': self.quote_name(old_field.column), 
                   'default': self.quote_value(self.effective_default(new_field))}
                mapping[new_field.column] = case_sql
            else:
                mapping[new_field.column] = self.quote_name(old_field.column)
            rename_mapping[old_field.name] = new_field.name
        if delete_field:
            del body[delete_field.name]
            del mapping[delete_field.column]
            if delete_field.many_to_many and delete_field.remote_field.through._meta.auto_created:
                return self.delete_model(delete_field.remote_field.through)
        apps = Apps()
        body = copy.deepcopy(body)
        unique_together = [ [ rename_mapping.get(n, n) for n in unique ] for unique in model._meta.unique_together
                          ]
        index_together = [ [ rename_mapping.get(n, n) for n in index ] for index in model._meta.index_together
                         ]
        indexes = model._meta.indexes
        if delete_field:
            indexes = [ index for index in indexes if delete_field.name not in index.fields
                      ]
        meta_contents = {'app_label': model._meta.app_label, 
           'db_table': model._meta.db_table, 
           'unique_together': unique_together, 
           'index_together': index_together, 
           'indexes': indexes, 
           'apps': apps}
        meta = type('Meta', tuple(), meta_contents)
        body['Meta'] = meta
        body['__module__'] = model.__module__
        temp_model = type(model._meta.object_name, model.__bases__, body)

        @contextlib.contextmanager
        def altered_table_name(model, temporary_table_name):
            original_table_name = model._meta.db_table
            model._meta.db_table = temporary_table_name
            yield
            model._meta.db_table = original_table_name

        with altered_table_name(model, model._meta.db_table + '__old'):
            self.alter_db_table(model, temp_model._meta.db_table, model._meta.db_table)
            self.deferred_sql = [ x for x in self.deferred_sql if temp_model._meta.db_table not in x ]
            self.create_model(temp_model)
            field_maps = list(mapping.items())
            self.execute('INSERT INTO %s (%s) SELECT %s FROM %s' % (
             self.quote_name(temp_model._meta.db_table),
             (', ').join(self.quote_name(x) for x, y in field_maps),
             (', ').join(y for x, y in field_maps),
             self.quote_name(model._meta.db_table)))
            self.delete_model(model, handle_autom2m=False)
        for sql in self.deferred_sql:
            self.execute(sql)

        self.deferred_sql = []
        if restore_pk_field:
            restore_pk_field.primary_key = True
        return

    def delete_model(self, model, handle_autom2m=True):
        if handle_autom2m:
            super(DatabaseSchemaEditor, self).delete_model(model)
        else:
            self.execute(self.sql_delete_table % {'table': self.quote_name(model._meta.db_table)})

    def add_field(self, model, field):
        """
        Creates a field on a model.
        Usually involves adding a column, but may involve adding a
        table instead (for M2M fields)
        """
        if field.many_to_many and field.remote_field.through._meta.auto_created:
            return self.create_model(field.remote_field.through)
        self._remake_table(model, create_field=field)

    def remove_field(self, model, field):
        """
        Removes a field from a model. Usually involves deleting a column,
        but for M2Ms may involve deleting a table.
        """
        if field.many_to_many:
            if field.remote_field.through._meta.auto_created:
                self.delete_model(field.remote_field.through)
        else:
            if field.db_parameters(connection=self.connection)['type'] is None:
                return
            self._remake_table(model, delete_field=field)
        return

    def _alter_field(self, model, old_field, new_field, old_type, new_type, old_db_params, new_db_params, strict=False):
        """Actually perform a "physical" (non-ManyToMany) field update."""
        self._remake_table(model, alter_field=(old_field, new_field))

    def _alter_many_to_many(self, model, old_field, new_field, strict):
        """
        Alters M2Ms to repoint their to= endpoints.
        """
        if old_field.remote_field.through._meta.db_table == new_field.remote_field.through._meta.db_table:
            self._remake_table(old_field.remote_field.through, alter_field=(
             old_field.remote_field.through._meta.get_field(old_field.m2m_reverse_field_name()),
             new_field.remote_field.through._meta.get_field(new_field.m2m_reverse_field_name())))
            return
        self.create_model(new_field.remote_field.through)
        self.execute('INSERT INTO %s (%s) SELECT %s FROM %s' % (
         self.quote_name(new_field.remote_field.through._meta.db_table),
         (', ').join([
          'id',
          new_field.m2m_column_name(),
          new_field.m2m_reverse_name()]),
         (', ').join([
          'id',
          old_field.m2m_column_name(),
          old_field.m2m_reverse_name()]),
         self.quote_name(old_field.remote_field.through._meta.db_table)))
        self.delete_model(old_field.remote_field.through)
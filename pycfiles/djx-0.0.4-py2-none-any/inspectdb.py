# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/commands/inspectdb.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import keyword, re
from collections import OrderedDict
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.models.constants import LOOKUP_SEP
from django.utils.encoding import force_text

class Command(BaseCommand):
    help = b'Introspects the database tables in the given database and outputs a Django model module.'
    requires_system_checks = False
    db_module = b'django.db'

    def add_arguments(self, parser):
        parser.add_argument(b'table', action=b'store', nargs=b'*', type=str, help=b'Selects what tables or views should be introspected.')
        parser.add_argument(b'--database', action=b'store', dest=b'database', default=DEFAULT_DB_ALIAS, help=b'Nominates a database to introspect. Defaults to using the "default" database.')

    def handle(self, **options):
        try:
            for line in self.handle_inspection(options):
                self.stdout.write(b'%s\n' % line)

        except NotImplementedError:
            raise CommandError(b"Database inspection isn't supported for the currently selected database backend.")

    def handle_inspection(self, options):
        connection = connections[options[b'database']]
        table_name_filter = options.get(b'table_name_filter')

        def table2model(table_name):
            return re.sub(b'[^a-zA-Z0-9]', b'', table_name.title())

        def strip_prefix(s):
            if s.startswith(b"u'"):
                return s[1:]
            return s

        with connection.cursor() as (cursor):
            yield b'# This is an auto-generated Django model module.'
            yield b"# You'll have to do the following manually to clean this up:"
            yield b"#   * Rearrange models' order"
            yield b'#   * Make sure each model has one field with primary_key=True'
            yield b'#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.'
            yield b'#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table'
            yield b"# Feel free to rename the models, but don't rename db_table values or field names."
            yield b'from __future__ import unicode_literals'
            yield b''
            yield b'from %s import models' % self.db_module
            known_models = []
            tables_to_introspect = options[b'table'] or connection.introspection.table_names(cursor)
            for table_name in tables_to_introspect:
                if table_name_filter is not None and callable(table_name_filter):
                    if not table_name_filter(table_name):
                        continue
                try:
                    try:
                        relations = connection.introspection.get_relations(cursor, table_name)
                    except NotImplementedError:
                        relations = {}

                    try:
                        constraints = connection.introspection.get_constraints(cursor, table_name)
                    except NotImplementedError:
                        constraints = {}

                    primary_key_column = connection.introspection.get_primary_key_column(cursor, table_name)
                    unique_columns = [ c[b'columns'][0] for c in constraints.values() if c[b'unique'] and len(c[b'columns']) == 1
                                     ]
                    table_description = connection.introspection.get_table_description(cursor, table_name)
                except Exception as e:
                    yield b"# Unable to inspect table '%s'" % table_name
                    yield b'# The error was: %s' % force_text(e)
                    continue

                yield b''
                yield b''
                yield b'class %s(models.Model):' % table2model(table_name)
                known_models.append(table2model(table_name))
                used_column_names = []
                column_to_field_name = {}
                for row in table_description:
                    comment_notes = []
                    extra_params = OrderedDict()
                    column_name = row[0]
                    is_relation = column_name in relations
                    att_name, params, notes = self.normalize_col_name(column_name, used_column_names, is_relation)
                    extra_params.update(params)
                    comment_notes.extend(notes)
                    used_column_names.append(att_name)
                    column_to_field_name[column_name] = att_name
                    if column_name == primary_key_column:
                        extra_params[b'primary_key'] = True
                    elif column_name in unique_columns:
                        extra_params[b'unique'] = True
                    if is_relation:
                        rel_to = b'self' if relations[column_name][1] == table_name else table2model(relations[column_name][1])
                        if rel_to in known_models:
                            field_type = b'ForeignKey(%s' % rel_to
                        else:
                            field_type = b"ForeignKey('%s'" % rel_to
                    else:
                        field_type, field_params, field_notes = self.get_field_type(connection, table_name, row)
                        extra_params.update(field_params)
                        comment_notes.extend(field_notes)
                        field_type += b'('
                    if att_name == b'id' and extra_params == {b'primary_key': True}:
                        if field_type == b'AutoField(':
                            continue
                        elif field_type == b'IntegerField(' and not connection.features.can_introspect_autofield:
                            comment_notes.append(b'AutoField?')
                    if row[6]:
                        if field_type == b'BooleanField(':
                            field_type = b'NullBooleanField('
                        else:
                            extra_params[b'blank'] = True
                            extra_params[b'null'] = True
                    field_desc = b'%s = %s%s' % (
                     att_name,
                     b'' if b'.' in field_type else b'models.',
                     field_type)
                    if field_type.startswith(b'ForeignKey('):
                        field_desc += b', models.DO_NOTHING'
                    if extra_params:
                        if not field_desc.endswith(b'('):
                            field_desc += b', '
                        field_desc += (b', ').join(b'%s=%s' % (k, strip_prefix(repr(v))) for k, v in extra_params.items())
                    field_desc += b')'
                    if comment_notes:
                        field_desc += b'  # ' + (b' ').join(comment_notes)
                    yield b'    %s' % field_desc

                for meta_line in self.get_meta(table_name, constraints, column_to_field_name):
                    yield meta_line

        return

    def normalize_col_name(self, col_name, used_column_names, is_relation):
        """
        Modify the column name to make it Python-compatible as a field name
        """
        field_params = {}
        field_notes = []
        new_name = col_name.lower()
        if new_name != col_name:
            field_notes.append(b'Field name made lowercase.')
        if is_relation:
            if new_name.endswith(b'_id'):
                new_name = new_name[:-3]
            else:
                field_params[b'db_column'] = col_name
        new_name, num_repl = re.subn(b'\\W', b'_', new_name)
        if num_repl > 0:
            field_notes.append(b'Field renamed to remove unsuitable characters.')
        if new_name.find(LOOKUP_SEP) >= 0:
            while new_name.find(LOOKUP_SEP) >= 0:
                new_name = new_name.replace(LOOKUP_SEP, b'_')

            if col_name.lower().find(LOOKUP_SEP) >= 0:
                field_notes.append(b"Field renamed because it contained more than one '_' in a row.")
        if new_name.startswith(b'_'):
            new_name = b'field%s' % new_name
            field_notes.append(b"Field renamed because it started with '_'.")
        if new_name.endswith(b'_'):
            new_name = b'%sfield' % new_name
            field_notes.append(b"Field renamed because it ended with '_'.")
        if keyword.iskeyword(new_name):
            new_name += b'_field'
            field_notes.append(b'Field renamed because it was a Python reserved word.')
        if new_name[0].isdigit():
            new_name = b'number_%s' % new_name
            field_notes.append(b"Field renamed because it wasn't a valid Python identifier.")
        if new_name in used_column_names:
            num = 0
            while b'%s_%d' % (new_name, num) in used_column_names:
                num += 1

            new_name = b'%s_%d' % (new_name, num)
            field_notes.append(b'Field renamed because of name conflict.')
        if col_name != new_name and field_notes:
            field_params[b'db_column'] = col_name
        return (new_name, field_params, field_notes)

    def get_field_type(self, connection, table_name, row):
        """
        Given the database connection, the table name, and the cursor row
        description, this routine will return the given field type name, as
        well as any additional keyword parameters and notes for the field.
        """
        field_params = OrderedDict()
        field_notes = []
        try:
            field_type = connection.introspection.get_field_type(row[1], row)
        except KeyError:
            field_type = b'TextField'
            field_notes.append(b'This field type is a guess.')

        if type(field_type) is tuple:
            field_type, new_params = field_type
            field_params.update(new_params)
        if field_type == b'CharField' and row[3]:
            field_params[b'max_length'] = int(row[3])
        if field_type == b'DecimalField':
            if row[4] is None or row[5] is None:
                field_notes.append(b'max_digits and decimal_places have been guessed, as this database handles decimal fields as float')
                field_params[b'max_digits'] = row[4] if row[4] is not None else 10
                field_params[b'decimal_places'] = row[5] if row[5] is not None else 5
            else:
                field_params[b'max_digits'] = row[4]
                field_params[b'decimal_places'] = row[5]
        return (
         field_type, field_params, field_notes)

    def get_meta(self, table_name, constraints, column_to_field_name):
        """
        Return a sequence comprising the lines of code necessary
        to construct the inner Meta class for the model corresponding
        to the given database table name.
        """
        unique_together = []
        for index, params in constraints.items():
            if params[b'unique']:
                columns = params[b'columns']
                if len(columns) > 1:
                    tup = b'(' + (b', ').join(b"'%s'" % column_to_field_name[c] for c in columns) + b')'
                    unique_together.append(tup)

        meta = [
         b'',
         b'    class Meta:',
         b'        managed = False',
         b"        db_table = '%s'" % table_name]
        if unique_together:
            tup = b'(' + (b', ').join(unique_together) + b',)'
            meta += [b'        unique_together = %s' % tup]
        return meta
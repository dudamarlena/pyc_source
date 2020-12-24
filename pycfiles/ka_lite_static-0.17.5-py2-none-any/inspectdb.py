# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/management/commands/inspectdb.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import keyword, re
from optparse import make_option
from django.core.management.base import NoArgsCommand, CommandError
from django.db import connections, DEFAULT_DB_ALIAS
from django.utils import six

class Command(NoArgsCommand):
    help = b'Introspects the database tables in the given database and outputs a Django model module.'
    option_list = NoArgsCommand.option_list + (
     make_option(b'--database', action=b'store', dest=b'database', default=DEFAULT_DB_ALIAS, help=b'Nominates a database to introspect.  Defaults to using the "default" database.'),)
    requires_model_validation = False
    db_module = b'django.db'

    def handle_noargs(self, **options):
        try:
            for line in self.handle_inspection(options):
                self.stdout.write(b'%s\n' % line)

        except NotImplementedError:
            raise CommandError(b"Database inspection isn't supported for the currently selected database backend.")

    def handle_inspection(self, options):
        connection = connections[options.get(b'database')]
        table_name_filter = options.get(b'table_name_filter')
        table2model = lambda table_name: table_name.title().replace(b'_', b'').replace(b' ', b'').replace(b'-', b'')
        strip_prefix = lambda s: s.startswith(b"u'") and s[1:] or s
        cursor = connection.cursor()
        yield b'# This is an auto-generated Django model module.'
        yield b"# You'll have to do the following manually to clean this up:"
        yield b"#     * Rearrange models' order"
        yield b'#     * Make sure each model has one field with primary_key=True'
        yield b"# Feel free to rename the models, but don't rename db_table values or field names."
        yield b'#'
        yield b"# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'"
        yield b'# into your database.'
        yield b'from __future__ import unicode_literals'
        yield b''
        yield b'from %s import models' % self.db_module
        yield b''
        known_models = []
        for table_name in connection.introspection.table_names(cursor):
            if table_name_filter is not None and callable(table_name_filter):
                if not table_name_filter(table_name):
                    continue
            yield b'class %s(models.Model):' % table2model(table_name)
            known_models.append(table2model(table_name))
            try:
                relations = connection.introspection.get_relations(cursor, table_name)
            except NotImplementedError:
                relations = {}

            try:
                indexes = connection.introspection.get_indexes(cursor, table_name)
            except NotImplementedError:
                indexes = {}

            used_column_names = []
            for i, row in enumerate(connection.introspection.get_table_description(cursor, table_name)):
                comment_notes = []
                extra_params = {}
                column_name = row[0]
                is_relation = i in relations
                att_name, params, notes = self.normalize_col_name(column_name, used_column_names, is_relation)
                extra_params.update(params)
                comment_notes.extend(notes)
                used_column_names.append(att_name)
                if column_name in indexes:
                    if indexes[column_name][b'primary_key']:
                        extra_params[b'primary_key'] = True
                    elif indexes[column_name][b'unique']:
                        extra_params[b'unique'] = True
                if is_relation:
                    rel_to = relations[i][1] == table_name and b"'self'" or table2model(relations[i][1])
                    if rel_to in known_models:
                        field_type = b'ForeignKey(%s' % rel_to
                    else:
                        field_type = b"ForeignKey('%s'" % rel_to
                else:
                    field_type, field_params, field_notes = self.get_field_type(connection, table_name, row)
                    extra_params.update(field_params)
                    comment_notes.extend(field_notes)
                    field_type += b'('
                if att_name == b'id' and field_type == b'AutoField(' and extra_params == {b'primary_key': True}:
                    continue
                if row[6]:
                    extra_params[b'blank'] = True
                    if field_type not in ('TextField(', 'CharField('):
                        extra_params[b'null'] = True
                field_desc = b'%s = models.%s' % (att_name, field_type)
                if extra_params:
                    if not field_desc.endswith(b'('):
                        field_desc += b', '
                    field_desc += (b', ').join([ b'%s=%s' % (k, strip_prefix(repr(v))) for k, v in extra_params.items()
                                               ])
                field_desc += b')'
                if comment_notes:
                    field_desc += b' # ' + (b' ').join(comment_notes)
                yield b'    %s' % field_desc

            for meta_line in self.get_meta(table_name):
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
        if new_name.find(b'__') >= 0:
            while new_name.find(b'__') >= 0:
                new_name = new_name.replace(b'__', b'_')

            if col_name.lower().find(b'__') >= 0:
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
        field_params = {}
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
            field_params[b'max_length'] = row[3]
        if field_type == b'DecimalField':
            field_params[b'max_digits'] = row[4]
            field_params[b'decimal_places'] = row[5]
        return (field_type, field_params, field_notes)

    def get_meta(self, table_name):
        """
        Return a sequence comprising the lines of code necessary
        to construct the inner Meta class for the model corresponding
        to the given database table name.
        """
        return [
         b'    class Meta:',
         b"        db_table = '%s'" % table_name,
         b'']
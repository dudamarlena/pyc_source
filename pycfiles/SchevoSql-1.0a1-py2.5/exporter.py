# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevosql/exporter.py
# Compiled at: 2008-01-19 12:36:32
"""SQL exporter for Schevo databases.

For copyright, license, and warranty, see bottom of file.
"""
__svn__ = '$Id$'
__rev__ = '$Rev$'[6:-2]
from schevo.constant import UNASSIGNED
from schevosql.field import to_colspec, to_data

class Exporter(object):
    """Exports a Schevo root to a pickle stream."""

    def __init__(self, db, dialect='jet'):
        """Create an exporter instance.

        - `db`: An open Schevo database.
        - `dialect`: Currently, only 'jet' is supported.  In the future,
          'mysql', 'postgres', etc. may be supported.
        """
        self.db = db
        self.dialect = dialect

    def export_to(self, output, schema=True, data=True, drop_tables=False):
        """Uses export_gen to do a blocking export of an entire
        database."""
        for x in self.export_gen(output, schema, data, drop_tables):
            pass

    def export_gen(self, output, schema=True, data=True, drop_tables=False):
        """Export to file-like object, yielding tuples of integers
        (current_extent, total_extents) after each extent is exported.

        - `schema`: True if schema should be exported.
        - `data`: True if data should be exported.
        - `drop_tables`: True if 'DROP TABLE' statements should be written
           before 'CREATE TABLE' statements.
        """
        db = self.db
        dialect = self.dialect
        constraints = []
        extent_names = db.extent_names()
        processed = 0
        total = len(extent_names)
        for extent_name in extent_names:
            if extent_name == 'SchevoIcon':
                continue
            extent = db.extent(extent_name)
            if schema:
                EntityClass = extent._EntityClass
                if drop_tables:
                    statement = 'DROP TABLE `%s`;\n' % extent_name
                    output.write(statement)
                statements = [
                 'CREATE TABLE `%s` (' % extent_name]
                col_parts = ['%s_oid INTEGER' % extent_name,
                 '%s_rev INTEGER' % extent_name]
                for (f_name, FieldClass) in EntityClass._field_spec.iteritems():
                    field = FieldClass(None, f_name)
                    if not field.readonly and field.fget is None:
                        (specs, constrs) = to_colspec(dialect, field)
                        constrs = [ c.replace('{table}', extent_name) for c in constrs
                                  ]
                        specs = [ s.replace('{table}', extent_name) for s in specs
                                ]
                        col_parts.extend(specs)
                        constraints.extend(constrs)

                col_parts.append('PRIMARY KEY (`%s_oid`)' % extent_name)
                statements.append((', ').join(col_parts))
                statements.append(');\n')
                statement = ('').join(statements)
                output.write(statement)
            if data:
                for entity in extent.find():
                    col_names = [
                     '`%s_oid`' % extent_name,
                     '`%s_rev`' % extent_name]
                    col_values = [
                     str(entity.sys.oid),
                     str(entity.sys.rev)]
                    for (field_name, field) in entity.sys.fields(include_readonly_fget=False).iteritems():
                        if field._value is not UNASSIGNED:
                            data = to_data(dialect, field)
                            if data is not None:
                                (col_name, col_value) = data
                                col_name = col_name.replace('{table}', extent_name)
                                col_names.append(col_name)
                                col_values.append(col_value)

                    statement = 'INSERT INTO %s (%s) VALUES (%s);\n' % (
                     extent_name,
                     (', ').join(col_names),
                     (', ').join(col_values))
                    output.write(statement)

            processed += 1
            yield (processed, total)

        for constr in constraints:
            output.write(constr)

        return
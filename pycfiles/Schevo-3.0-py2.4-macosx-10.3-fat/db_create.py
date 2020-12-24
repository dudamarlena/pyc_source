# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/script/db_create.py
# Compiled at: 2007-03-21 14:34:41
"""Create database command.

For copyright, license, and warranty, see bottom of file.
"""
import os, schevo.database, schevo.icon, schevo.schema
from schevo.script.command import Command
from schevo.script.db_evolve import evolve_db
from schevo.script import opt
from schevo.script.path import package_path
usage = 'schevo db create [options] DBFILE\n\nDBFILE: The database file to create.\n\nAt a minimum, either the --app or the --schema option must be specified.\n'

def _parser():
    p = opt.parser(usage)
    p.add_option('-a', '--app', dest='app_path', help='Use application in PATH.', metavar='PATH', default=None)
    p.add_option('-c', '--icons', dest='icon_path', help='Use icons from PATH.', metavar='PATH', default=None)
    p.add_option('-i', '--import', dest='import_from', help='Import XML data previously exported to FILE.', metavar='FILE', default=None)
    p.add_option('-p', '--sample', dest='create_sample_data', help='Create sample data.', action='store_true', default=False)
    p.add_option('-s', '--schema', dest='schema_path', help='Use schema in PATH.', metavar='PATH', default=None)
    p.add_option('-v', '--version', dest='schema_version', help='Evolve database to VERSION.', metavar='VERSION', default='latest')
    p.add_option('-x', '--delete', dest='delete_existing_database', help='Delete existing database file if one exists.', action='store_true', default=False)
    return p


class Create(Command):
    __module__ = __name__
    name = 'Create Database'
    description = 'Create a new database.'

    def main(self, arg0, args):
        print
        print
        parser = _parser()
        (options, args) = parser.parse_args(list(args))
        if len(args) != 1:
            parser.error('Please specify DBFILE.')
        db_filename = args[0]
        icon_path = None
        schema_path = None
        if options.app_path:
            app_path = package_path(options.app_path)
            icon_path = os.path.join(app_path, 'icons')
            schema_path = os.path.join(app_path, 'schema')
        if options.icon_path:
            icon_path = package_path(options.icon_path)
        if options.schema_path:
            schema_path = package_path(options.schema_path)
        if schema_path is None:
            parser.error('Please specify either the --app or --schema option.')
        schema_source = schevo.schema.read(schema_path, version=1)
        if options.delete_existing_database:
            if os.path.isfile(db_filename):
                print 'Deleting existing file:', db_filename
                os.remove(db_filename)
        if os.path.isfile(db_filename):
            parser.error('Use "schevo db update" command to update an existing database.')
        print 'Creating new database...'
        if options.import_from is not None:
            print 'Importing data from %r...' % options.import_from
            try:
                import_file = open(options.import_from, 'r')
            except IOError:
                parser.error('Could not open XML data file %r' % options.import_from)
            else:
                db = schevo.database.open(db_filename, schema_source, initialize=False)
                from schevoxml import ImporterTransaction
                tx = ImporterTransaction(import_file)
                db.execute(tx)
                import_file.close()
        else:
            db = schevo.database.open(db_filename, schema_source)
        final_version = options.schema_version.lower()
        if final_version != 'latest':
            try:
                final_version = int(final_version)
            except ValueError:
                parser.error('Please specify a version number or "latest".')

        if final_version != 1:
            print 'Evolving database...'
            evolve_db(parser, schema_path, db, final_version)
        if icon_path and os.path.exists(icon_path):
            print 'Importing icons...'
            schevo.icon.install(db, icon_path)
        if options.create_sample_data:
            print 'Populating with sample data...'
            db.populate()
        print 'Packing the database...'
        db.pack()
        print 'Database version is now at %i.' % db.version
        db.close()
        print 'Database created.'
        return


start = Create
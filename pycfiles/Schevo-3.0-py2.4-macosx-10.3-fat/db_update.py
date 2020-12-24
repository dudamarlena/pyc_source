# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/script/db_update.py
# Compiled at: 2007-03-21 14:34:41
"""Update database command.

For copyright, license, and warranty, see bottom of file.
"""
import os, schevo.database, schevo.error, schevo.icon, schevo.schema
from schevo.script.command import Command
from schevo.script import opt
from schevo.script.path import package_path
usage = 'schevo db update [options] DBFILE\n\nDBFILE: The database file to update.\n\nAt a minimum, either the --app or the --schema option must be specified.\n'

def _parser():
    p = opt.parser(usage)
    p.add_option('-a', '--app', dest='app_path', help='Use application in PATH.', metavar='PATH', default=None)
    p.add_option('-c', '--icons', dest='icon_path', help='Use icons from PATH.', metavar='PATH', default=None)
    p.add_option('-s', '--schema', dest='schema_path', help='Use schema in PATH.', metavar='PATH', default=None)
    return p


class Update(Command):
    __module__ = __name__
    name = 'Update Database'
    description = 'Update an existing database.'

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
        if not os.path.isfile(db_filename):
            parser.error('DBFILE must be an existing database.')
        print 'Opening database...'
        db = schevo.database.open(db_filename)
        print 'Current database version is %i.' % db.version
        try:
            schema_source = schevo.schema.read(schema_path, version=db.version)
        except schevo.error.SchemaFileIOError:
            parser.error('Could not read schema source for version %i.' % db.version)

        print 'Syncing database with new schema source...'
        db._sync(schema_source, initialize=False)
        if icon_path and os.path.exists(icon_path):
            print 'Importing icons...'
            schevo.icon.install(db, icon_path)
        print 'Packing the database...'
        db.pack()
        db.close()
        print 'Database updated.'
        return


start = Update
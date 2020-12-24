# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/script/db_evolve.py
# Compiled at: 2007-03-21 14:34:41
"""Evolve database command.

For copyright, license, and warranty, see bottom of file.
"""
import os, schevo.database, schevo.error, schevo.icon, schevo.schema
from schevo.script.command import Command
from schevo.script import opt
from schevo.script.path import package_path
usage = "schevo db evolve [options] DBFILE VERSION\n\nDBFILE: The database file to evolve.\n\nVERSION: The version of the schema to evolve to.  The database will be\nevolved as many times as necessary to reach the version specified.\nSpecifying 'latest' causes the database to be evolved to the latest\nschema version available.\n\nAt a minimum, either the --app or the --schema option must be specified.\n"

def _parser():
    p = opt.parser(usage)
    p.add_option('-a', '--app', dest='app_path', help='Use application in PATH.', metavar='PATH', default=None)
    p.add_option('-c', '--icons', dest='icon_path', help='Use icons from PATH.', metavar='PATH', default=None)
    p.add_option('-s', '--schema', dest='schema_path', help='Use schema in PATH.', metavar='PATH', default=None)
    return p


class Evolve(Command):
    __module__ = __name__
    name = 'Evolve Database'
    description = 'Evolve an existing database.'

    def main(self, arg0, args):
        print
        print
        parser = _parser()
        (options, args) = parser.parse_args(list(args))
        if len(args) != 2:
            parser.error('Please specify both DBFILE and VERSION.')
        (db_filename, final_version) = args
        final_version = final_version.lower()
        if final_version != 'latest':
            try:
                final_version = int(final_version)
            except ValueError:
                parser.error('Please specify a version number or "latest".')

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
        db = schevo.database.open(db_filename)
        print 'Current database version is %i.' % db.version
        evolve_db(parser, schema_path, db, final_version)
        if icon_path and os.path.exists(icon_path):
            print 'Importing icons...'
            schevo.icon.install(db, icon_path)
        print 'Packing the database...'
        db.pack()
        db.close()
        print 'Database created.'
        return


start = Evolve

def evolve_db(parser, schema_path, db, final_version):
    if isinstance(final_version, int) and final_version <= db.version:
        db.close()
        parser.error('Version specified is <= current database version.')
    version = db.version + 1
    schemata_source = {}
    while version <= final_version or final_version == 'latest':
        try:
            source = schevo.schema.read(schema_path, version=version)
        except schevo.error.SchemaFileIOError:
            if final_version == 'latest':
                break
            parser.error('Could not read version %i' % version)

        schemata_source[version] = source
        print 'Read schema source for version %i.' % version
        version += 1

    versions = sorted(schemata_source.keys())
    if final_version == 'latest' and not versions:
        print 'Database is already at latest version.'
        return 0
    for version in versions:
        print 'Evolving database to version %i...' % version
        source = schemata_source[version]
        try:
            db._evolve(source, version)
        except:
            print 'Evolution to version %i failed.' % version
            print 'Database was left at version %i.' % db.version
            print 'Traceback of evolution failure follows.'
            db.close()
            raise

    print 'Database evolution to version %i complete.' % db.version
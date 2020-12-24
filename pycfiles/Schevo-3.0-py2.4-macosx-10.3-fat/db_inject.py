# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/script/db_inject.py
# Compiled at: 2007-03-21 14:34:41
"""Inject schema into database.

For copyright, license, and warranty, see bottom of file.
"""
import os, schevo.database, schevo.icon, schevo.schema
from schevo.script.command import Command
from schevo.script import opt
usage = 'schevo db inject [options] DBFILE\n\nDBFILE: The database file to inject a schema into.\n\nTHIS IS A DANGEROUS COMMAND and should only be used when absolutely\nnecessary.  When injecting a new schema into a database, it should not\nhave any changes that alter the semantics of the schema.\n\nEither --app or --schema must be given at a minimum.\n\nNote: Currently, only the schema_001.py file will be loaded from the\nschema package.'

def _parser():
    p = opt.parser(usage)
    p.add_option('-a', '--app', dest='app_path', help='Use application in PATH.', metavar='PATH', default=None)
    p.add_option('-s', '--schema', dest='schema_path', help='Use schema in PATH.', metavar='PATH', default=None)
    return p


class Inject(Command):
    __module__ = __name__
    name = 'Inject Schema'
    description = 'Inject schema into an existing database.'

    def main(self, arg0, args):
        print
        print
        parser = _parser()
        (options, args) = parser.parse_args(list(args))
        if len(args) != 1:
            parser.error('Please specify DBFILE.')
        db_filename = args[0]

        def path(pkg_or_path):
            """If pkg_or_path is a module, return its path; otherwise,
            return pkg_or_path."""
            from_list = pkg_or_path.split('.')[:1]
            try:
                pkg = __import__(pkg_or_path, {}, {}, from_list)
            except ImportError:
                return pkg_or_path

            if '__init__.py' in pkg.__file__:
                return os.path.dirname(pkg.__file__)
            else:
                return pkg.__file__

        schema_path = None
        if options.app_path:
            app_path = path(options.app_path)
            schema_path = os.path.join(app_path, 'schema')
        if options.schema_path:
            schema_path = path(options.schema_path)
        schema_source = schevo.schema.read(schema_path, version=1)
        schema_version = 1
        if not os.path.isfile(db_filename):
            parser.error('Please specify a DBFILE that exists.')
        schevo.database.inject(db_filename, schema_source, schema_version)
        print 'Schema injected.'
        return


start = Inject
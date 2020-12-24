# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/kolekto/commands/restore.py
# Compiled at: 2014-06-16 16:12:17
import json
from kolekto.printer import printer
from kolekto.commands import Command

class Restore(Command):
    """ Restore metadata from a json dump.
    """
    help = 'Restore metadata from a json dump'

    def prepare(self):
        self.add_arg('file', help='The json dump file to restore')

    def run(self, args, config):
        mdb = self.get_metadata_db(args.tree)
        with open(args.file) as (fdump):
            dump = json.load(fdump)
        for movie in dump:
            mdb.save(movie['hash'], movie['movie'])
            printer.verbose('Loaded {hash}', hash=movie['hash'])

        printer.p('Loaded {nb} movies.', nb=len(dump))
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/kolekto/commands/rm.py
# Compiled at: 2014-06-16 16:12:17
from kolekto.commands import Command
from kolekto.printer import printer
from kolekto.helpers import get_hash

class Rm(Command):
    """ Remove a movie from the kolekto tree.
    """
    help = 'remove a movie'

    def prepare(self):
        self.add_arg('input', metavar='movie-hash-or-file')

    def run(self, args, config):
        mdb = self.get_metadata_db(args.tree)
        movie_hash = get_hash(args.input)
        try:
            mdb.get(movie_hash)
        except KeyError:
            printer.p('Unknown movie hash.')
            return

        if printer.ask('Are you sure?', default=False):
            mdb.remove(movie_hash)
            printer.p('Removed. You need to launch gc to free space.')
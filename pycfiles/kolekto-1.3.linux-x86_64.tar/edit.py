# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/kolekto/commands/edit.py
# Compiled at: 2014-06-16 16:12:17
import json
from kolekto.printer import printer
from kolekto.commands import Command
from kolekto.helpers import get_hash

class Edit(Command):
    """ Edit a movie.
    """
    help = 'edit a movie'

    def prepare(self):
        self.add_arg('input', metavar='movie-hash-or-file')

    def run(self, args, config):
        mdb = self.get_metadata_db(args.tree)
        movie_hash = get_hash(args.input)
        try:
            movie = mdb.get(movie_hash)
        except KeyError:
            printer.p('Unknown movie hash.')
            return

        movie_json = json.dumps(movie, indent=4)
        while True:
            movie_json = printer.edit(movie_json)
            try:
                mdb.save(movie_hash, json.loads(movie_json))
            except ValueError:
                if printer.ask('Bad json data, would you like to try again?', default=True):
                    continue
                else:
                    break
            else:
                printer.p('Saved.')
                break
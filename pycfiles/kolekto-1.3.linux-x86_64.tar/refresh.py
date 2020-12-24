# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/kolekto/commands/refresh.py
# Compiled at: 2014-06-16 16:12:17
from kolekto.printer import printer
from kolekto.commands import Command
from kolekto.datasources import MovieDatasource
from kolekto.commands.show import show
from kolekto.helpers import get_hash

class Refresh(Command):
    """ Refresh metadata of movies.
    """
    help = 'refresh metadata of movies'

    def prepare(self):
        self.add_arg('input', metavar='movie-hash-or-file', nargs='?', help='Hash or path of the movie to refresh. If not specified, refresh all movies.')

    def run(self, args, config):
        mdb = self.get_metadata_db(args.tree)
        mds = MovieDatasource(config.subsections('datasource'), args.tree, self.profile.object_class)
        if args.input is None:
            if printer.ask('Would you like to refresh all movies?', default=True):
                with printer.progress(mdb.count(), task=True) as (update):
                    for movie_hash, movie in list(mdb.itermovies()):
                        movie = mds.refresh(movie)
                        mdb.save(movie_hash, movie)
                        printer.verbose('Saved {hash}', hash=movie_hash)
                        update(1)

        else:
            movie_hash = get_hash(args.input)
            try:
                movie = mdb.get(movie_hash)
            except KeyError:
                printer.p('Unknown movie hash.')
                return

        movie = mds.refresh(movie)
        show(movie)
        if printer.ask('Would you like to save the movie?', default=True):
            mdb.save(movie_hash, movie)
            printer.p('Saved.')
        return
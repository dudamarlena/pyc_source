# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/kolekto/commands/show.py
# Compiled at: 2014-06-16 16:12:17
from kolekto.commands import Command
from kolekto.datasources import MovieDatasource
from kolekto.printer import printer
from kolekto.helpers import get_hash
METADATA_SORTER_FIRST = ('title', 'year', 'directors', 'cast', 'writers', 'collection',
                         'genres')

def show(movie):
    """ Show the movie metadata.
    """
    for key, value in sorted(movie.iteritems(), cmp=metadata_sorter, key=lambda x: x[0]):
        if isinstance(value, list):
            if not value:
                continue
            other = value[1:]
            value = value[0]
        else:
            other = []
        printer.p('<b>{key}</b>: {value}', key=key, value=value)
        for value in other:
            printer.p('{pad}{value}', value=value, pad=' ' * (len(key) + 2))


def metadata_sorter(x, y):
    """ Sort metadata keys by priority.
    """
    if x == y:
        return 0
    else:
        if x in METADATA_SORTER_FIRST and y in METADATA_SORTER_FIRST:
            if METADATA_SORTER_FIRST.index(x) < METADATA_SORTER_FIRST.index(y):
                return -1
            return 1
        if x in METADATA_SORTER_FIRST:
            return -1
        if y in METADATA_SORTER_FIRST:
            return 1
        if x.startswith('_') and y.startswith('_'):
            return cmp(x[1:], y[1:])
        if x.startswith('_'):
            return 1
        if y.startswith('_'):
            return -1
        return cmp(x, y)


class Show(Command):
    """ Show information about movies.
    """
    help = 'show informations about a movie'

    def prepare(self):
        self.add_arg('input', metavar='movie-hash-or-file')

    def run(self, args, config):
        mdb = self.get_metadata_db(args.tree)
        mds = MovieDatasource(config.subsections('datasource'), args.tree, self.profile.object_class)
        movie_hash = get_hash(args.input)
        try:
            movie = mdb.get(movie_hash)
        except KeyError:
            printer.p('Unknown movie hash.')
            return

        movie = mds.attach(movie_hash, movie)
        show(movie)
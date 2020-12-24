# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/freedev/Desktop/supermovies/supermovies/playlist.py
# Compiled at: 2016-09-30 09:09:16
# Size of source mod 2**32: 2172 bytes
from . import Movie
from . import Reviewer, WaldorfAndStatler
from . import SnackBar

class Playlist:

    def __init__(self, name, reviewer=WaldorfAndStatler):
        self._Playlist__name = name
        self._Playlist__movies = []
        self.set_reviewer(reviewer)

    def load(self, from_file='movies.csv'):
        with open(from_file) as (file):
            for line in file:
                movie = Movie.from_csv(line)
                self._Playlist__movies.append(movie)

    def save(self, to_file='movie_rankings.csv'):
        with open(to_file, 'w') as (file):
            for movie in sorted(self._Playlist__movies):
                file.write(movie.to_csv() + '\n')

    def set_reviewer(self, reviewer):
        if not issubclass(reviewer, Reviewer):
            raise TypeError('You must pass a Reviewer class')
        else:
            self._Playlist__reviewer = reviewer

    def add_movie(self, movie):
        self._Playlist__movies.append(movie)

    def play(self, viewings):
        print("%s's playlist:" % self._Playlist__name)
        print(sorted(self._Playlist__movies))
        snacks = SnackBar.SNACKS
        print('There are {} available in the snack bar.'.format(len(snacks)))
        for snack in snacks:
            print('{} has {} carbs'.format(snack.name, snack.carbs))

        for count in range(0, viewings):
            print('\nViewings: %d' % (count + 1))
            for movie in self._Playlist__movies:
                self._Playlist__reviewer.review(movie)
                snack = SnackBar.random()
                movie.ate_snack(snack)
                print(movie)

    def total_carbs_consumed(self):
        result = 0
        for movie in self._Playlist__movies:
            result += movie.carbs_consumed()

        return result

    def print_stats(self):
        print("\n%s's Stats:" % self._Playlist__name)
        print('{} total carbs consumed'.format(self.total_carbs_consumed()))
        for movie in sorted(self._Playlist__movies):
            print("\n{}'s snacks total:".format(movie.get_title()))
            for snack in movie.snacks():
                print('{} total {} carbs'.format(snack.carbs, snack.name))

            print('{} grand total carbs'.format(movie.carbs_consumed()))

        hits = [movie for movie in self._Playlist__movies if movie.is_a_hit()]
        flops = [movie for movie in self._Playlist__movies if movie not in hits]
        print('\nHits:')
        for hit in hits:
            print(hit)

        print('\nFlops:')
        for flop in flops:
            print(flop)
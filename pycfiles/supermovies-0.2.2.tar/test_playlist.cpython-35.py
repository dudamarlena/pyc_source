# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/freedev/Desktop/supermovies/supermovies/tests/test_playlist.py
# Compiled at: 2016-09-30 09:05:00
# Size of source mod 2**32: 969 bytes
import unittest
from supermovies import Die, Movie, Playlist

class TestPlaylistBeingPlayedWithOneMovie(unittest.TestCase):

    def setUp(self):
        self.playlist = Playlist('Kermit')
        self.times = 3
        self.initial_rank = 10
        self.movie = Movie('Goonies', self.initial_rank)
        self.playlist.add_movie(self.movie)

    def test_movie_got_a_thumbs_up_if_a_high_number_is_rolled(self):
        Die.roll = lambda : 5
        self.playlist.play(self.times)
        self.assertEqual(self.movie.get_rank(), self.initial_rank + self.times)

    def test_movie_got_skipped_if_a_medium_number_is_rolled(self):
        Die.roll = lambda : 3
        self.playlist.play(self.times)
        self.assertEqual(self.movie.get_rank(), self.initial_rank)

    def test_movie_got_a_thumbs_down_if_a_low_number_is_rolled(self):
        Die.roll = lambda : 1
        self.playlist.play(self.times)
        self.assertEqual(self.movie.get_rank(), self.initial_rank - self.times)


if __name__ == '__main__':
    unittest.main()
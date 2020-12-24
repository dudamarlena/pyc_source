# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/freedev/Desktop/supermovies/supermovies/movie3d.py
# Compiled at: 2016-09-30 09:08:01
# Size of source mod 2**32: 528 bytes
from . import Movie

class Movie3D(Movie):

    def __init__(self, title, rank, wow_factor):
        super().__init__(title, rank)
        self._wow_factor = wow_factor

    def thumbs_up(self):
        for i in range(0, self._wow_factor):
            super().thumbs_up()

    def show_effect(self):
        print('Wow! ' * self._wow_factor)


if __name__ == '__main__':
    movie3d = Movie3D('glee', 5, 20)
    print(movie3d.get_title())
    print(movie3d.get_rank())
    movie3d.thumbs_up()
    print(movie3d.get_rank())
    print(movie3d)
    movie3d.show_effect()
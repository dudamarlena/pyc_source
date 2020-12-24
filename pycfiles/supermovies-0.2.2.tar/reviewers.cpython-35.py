# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/freedev/Desktop/supermovies/supermovies/reviewers.py
# Compiled at: 2016-09-30 09:09:23
# Size of source mod 2**32: 848 bytes
from random import randint
from abc import ABC, abstractmethod
from . import Die

class Reviewer(ABC):

    @classmethod
    @abstractmethod
    def review(cls, movie):
        raise NotImplementedError


class WaldorfAndStatler(Reviewer):

    @classmethod
    def review(cls, movie):
        number_rolled = Die.roll()
        if number_rolled < 3:
            movie.thumbs_down()
            print('%s got a thumbs down.' % movie.get_title())
        else:
            if number_rolled < 5:
                print('%s was skipped!' % movie.get_title())
            else:
                movie.thumbs_up()
                print('%s got a thumbs up!' % movie.get_title())


class BadMan(Reviewer):

    @classmethod
    def review(cls, movie):
        number_rolled = Die.roll()
        if number_rolled == 6:
            print('%s was skipped!' % movie.get_title())
        else:
            movie.thumbs_down()
            print('%s got a thumbs down.' % movie.get_title())
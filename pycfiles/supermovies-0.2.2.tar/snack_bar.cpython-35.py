# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/freedev/Desktop/supermovies/supermovies/snack_bar.py
# Compiled at: 2016-09-30 08:26:17
# Size of source mod 2**32: 628 bytes
from random import choice
from collections import namedtuple
Snack = namedtuple('Snack', ('name', 'carbs'))

class SnackBar:
    SNACKS = [
     Snack('popcorn', 20),
     Snack('candy', 15),
     Snack('nachos', 40),
     Snack('pretzel', 10),
     Snack('soda', 5)]

    @classmethod
    def random(cls):
        return choice(cls.SNACKS)


if __name__ == '__main__':
    popcorn = Snack('popcorn', 20)
    print(popcorn.name)
    print(popcorn.carbs)
    candy = Snack('candy', 15)
    print(candy.name)
    print(candy.carbs)
    print(SnackBar.SNACKS)
    snack = SnackBar.random()
    print('Enjoy your {} ({} carbs)'.format(snack.name, snack.carbs))
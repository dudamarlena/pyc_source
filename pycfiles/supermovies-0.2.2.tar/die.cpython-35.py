# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/freedev/Desktop/supermovies/supermovies/die.py
# Compiled at: 2016-09-30 04:23:27
# Size of source mod 2**32: 95 bytes
from random import randint

class Die:

    @classmethod
    def roll(cls):
        return randint(1, 6)
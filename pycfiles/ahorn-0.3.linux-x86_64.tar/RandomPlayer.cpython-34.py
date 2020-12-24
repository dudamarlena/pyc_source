# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/iii/Documents/projects/ahorn/venv/lib/python3.4/site-packages/ahorn/Actors/RandomPlayer.py
# Compiled at: 2016-08-02 10:00:55
# Size of source mod 2**32: 237 bytes
from . import RandomActor
from ..GameBase import Player

class RandomPlayer(RandomActor, Player):
    __doc__ = 'A player who takes a random action from the list of legal actions.'

    def __str__(self):
        return 'RandomPlayer'
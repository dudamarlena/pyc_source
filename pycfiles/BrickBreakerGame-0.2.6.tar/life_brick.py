# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: BrickBreaker/Bricks/life_brick.py
# Compiled at: 2017-12-13 09:34:09
from BrickBreaker.Bricks import Brick
from BrickBreaker.Shared import *

class LifeBrick(Brick):

    def __init__(self, position, image, game):
        super().__init__(position, image, game)

    def hit(self):
        game = self.get_game()
        game.add_one_life()
        super().hit()

    @staticmethod
    def get_hit_sound():
        return GameConstants.SOUND_HIT_EXTRA_LIFE
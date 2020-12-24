# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/uros/Projects/BrickBreaker/BrickBreaker/Bricks/size_brick.py
# Compiled at: 2017-12-13 09:34:09
# Size of source mod 2**32: 523 bytes
from BrickBreaker.Bricks import Brick
from BrickBreaker.Shared import *
from BrickBreaker.pad import Pad

class SizeBrick(Brick):

    def __init__(self, position, image, game):
        super().__init__(position, image, game)

    def hit(self):
        game = self.get_game()
        if isinstance(game.get_pad(), Pad):
            game.double_pad()
        else:
            game.increase_score_by_1k()
        super().hit()

    @staticmethod
    def get_hit_sound():
        return GameConstants.SOUND_HIT_BONUS_SIZE
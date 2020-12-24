# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
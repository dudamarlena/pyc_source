# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/uros/Projects/BrickBreaker/BrickBreaker/Bricks/speed_brick.py
# Compiled at: 2017-12-13 09:34:09
# Size of source mod 2**32: 450 bytes
from BrickBreaker.Bricks import Brick
from BrickBreaker.Shared import *

class SpeedBrick(Brick):

    def __init__(self, position, image, game):
        super().__init__(position, image, game)

    def hit(self):
        game = self.get_game()
        for ball in game.get_balls():
            ball.set_speed(ball.get_speed() + 1)

        super().hit()

    @staticmethod
    def get_hit_sound():
        return GameConstants.SOUND_HIT_SPEED_UP
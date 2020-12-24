# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: BrickBreaker/Bricks/brick.py
# Compiled at: 2017-12-13 09:34:09
from BrickBreaker.Shared import GameObject
from BrickBreaker.Shared import GameConstants

class Brick(GameObject):

    def __init__(self, position, image, game):
        self._game = game
        self._hit_points = 100
        self._lives = 1
        super().__init__(position, GameConstants.BRICK_SIZE, image)

    def get_game(self):
        return self._game

    def is_destroyed(self):
        return self._lives < 1

    def get_hit_points(self):
        return self._hit_points

    def hit(self):
        self._lives -= 1

    @staticmethod
    def get_hit_sound():
        return GameConstants.SOUND_HIT_BRICK
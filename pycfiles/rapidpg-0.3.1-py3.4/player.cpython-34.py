# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rapidpg\types\player.py
# Compiled at: 2014-07-08 21:53:57
# Size of source mod 2**32: 1448 bytes
from .animation import Animated, Animation
from pygame.rect import Rect

class Player(Animated):
    __doc__ = "\n    An instance is compatible with the level manager. Note that if\n    :func:`rapidpg.levelmgr.collision.Level.update` is not used, a player\n    instance doesn't have to be passed to the level manager\n    "

    def __init__(self, surfs, interval):
        """
        :param surfs: A list of surfaces for animation
        :param interval: The interval between animation updates
        """
        super(Player, self).__init__({'right': Animation(surfs, interval)}, lambda : 'right', 'right')
        self.jump_frames_left = 0
        self.jumping = False
        self.in_air = False
        self.up_speed = 20
        self.down_speed = 0
        self.dir = 'right'
        self.surfs = surfs
        self.rect = Rect(0, 0, 0, 0)
        if surfs:
            self.rect = surfs[0].get_rect()
        self.animation_interval = interval
        self.speed = 7

    def move(self, x, y):
        """
        Alias for ``plr.rect.move_ip``
        """
        self.rect.move_ip(x, y)

    def start_jump(self):
        """
        This method is used by the level manager to start the jump
        """
        if not self.jumping:
            self.jumping = True
            self.in_air = True
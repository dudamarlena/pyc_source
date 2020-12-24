# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\研发资料\瓦力课程\试听课\代码\dianyi\camera.py
# Compiled at: 2019-08-09 05:45:32
# Size of source mod 2**32: 1724 bytes
from .config import *
from .draw_options import NewDrawOptions

class Camera:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self, size=None):
        if size:
            self.surface = pygame.Surface(size)
            self.scl = 1
            self._position = vec(0, 0)
            self._subject = None
            self.draw_options = NewDrawOptions(self.surface)
        else:
            self = global_var.CAMERA

    @property
    def size(self):
        return self.surface.get_size()

    def update(self):
        self.surface.fill((255, 255, 255))
        if self._subject:
            self._position = self._subject.pos
        global_var.ALL_SPRITES.update()
        rects = global_var.ALL_SPRITES.draw(self.surface)
        if global_var.DEBUG_DRAW:
            global_var.SPACE.debug_draw(self.draw_options)

    def follow(self, subject):
        self._subject = subject

    def scale(self, s):
        self.scl = s

    @property
    def offset(self):
        return (-self._position[0], self._position[1])

    @property
    def x(self):
        return self._position[0]

    @property
    def y(self):
        return self._position[1]

    @property
    def pos(self):
        return self._position

    @x.setter
    def x(self, x):
        self._position[0] = x

    @y.setter
    def y(self, y):
        self._position[1] = y

    @pos.setter
    def pos(self, pos):
        self._position = pos
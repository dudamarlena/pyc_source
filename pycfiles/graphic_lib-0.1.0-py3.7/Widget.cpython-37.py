# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\graphic_lib\detail\Widget.py
# Compiled at: 2020-02-16 11:49:42
# Size of source mod 2**32: 317 bytes
from abc import ABC
from abc import abstractmethod
from graphic_lib.detail import Drawable
from graphic_lib.Display import Color

class Widget(ABC, Drawable):

    def __init__(self, size):
        Drawable.__init__(self, size, Color(0, 0, 0))

    @abstractmethod
    def update(self):
        pass
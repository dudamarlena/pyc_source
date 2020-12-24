# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\cocos\scenes\pause.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 3950 bytes
__doc__ = 'Pause scene'
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import cocos.director as director
from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene
import pyglet
from pyglet.gl import *
__pause_scene_generator__ = None

def get_pause_scene():
    global __pause_scene_generator__
    return __pause_scene_generator__()


def set_pause_scene_generator(generator):
    global __pause_scene_generator__
    __pause_scene_generator__ = generator


def default_pause_scene():
    w, h = director.window.width, director.window.height
    texture = pyglet.image.Texture.create_for_size(GL_TEXTURE_2D, w, h, GL_RGBA)
    texture.blit_into(pyglet.image.get_buffer_manager().get_color_buffer(), 0, 0, 0)
    return PauseScene(texture.get_region(0, 0, w, h), ColorLayer(25, 25, 25, 205), PauseLayer())


set_pause_scene_generator(default_pause_scene)

class PauseScene(Scene):
    """PauseScene"""

    def __init__(self, background, *layers):
        (super(PauseScene, self).__init__)(*layers)
        self.bg = background
        self.width, self.height = director.get_window_size()

    def draw(self):
        self.bg.blit(0, 0, width=(self.width), height=(self.height))
        super(PauseScene, self).draw()


class PauseLayer(Layer):
    """PauseLayer"""
    is_event_handler = True

    def __init__(self):
        super(PauseLayer, self).__init__()
        x, y = director.get_window_size()
        self.label = pyglet.text.Label('PAUSED', font_name='Arial', font_size=36, width=x,
          height=y,
          align='center',
          x=(x // 2),
          y=(y // 2))
        self.label.x = (x - self.label.content_width) // 2

    def draw(self):
        self.label.draw()

    def on_key_press(self, k, m):
        if k == pyglet.window.key.P:
            if m & pyglet.window.key.MOD_ACCEL:
                director.pop()
                return True
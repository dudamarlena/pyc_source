# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\samples\tetrico\gamectrl.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2850 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
import copy, random, pyglet
from pyglet.window import key
from cocos.layer import Layer
from cocos.scene import Scene
from cocos.euclid import Point2
from constants import *
from status import status
__all__ = [
 'GameCtrl']

class GameCtrl(Layer):
    is_event_handler = True

    def __init__(self, model):
        super(GameCtrl, self).__init__()
        self.used_key = False
        self.paused = True
        self.model = model
        self.elapsed = 0

    def on_key_press(self, k, m):
        if self.paused:
            return False
        else:
            if self.used_key:
                return False
                if k in (key.LEFT, key.RIGHT, key.DOWN, key.UP, key.SPACE):
                    if k == key.LEFT:
                        self.model.block_left()
            elif k == key.RIGHT:
                self.model.block_right()
            elif k == key.DOWN:
                self.model.block_down()
            elif k == key.UP:
                self.model.block_rotate()
            elif k == key.SPACE:
                self.elapsed = 0
                self.model.block_drop()
            self.used_key = True
            return True
        return False

    def on_text_motion(self, motion):
        if self.paused:
            return False
        else:
            if self.used_key:
                return False
                if motion in (key.MOTION_DOWN, key.MOTION_RIGHT, key.MOTION_LEFT):
                    if motion == key.MOTION_DOWN:
                        self.model.block_down()
            elif motion == key.MOTION_LEFT:
                self.model.block_left()
            elif motion == key.MOTION_RIGHT:
                self.model.block_right()
            self.used_key = True
            return True
        return False

    def pause_controller(self):
        """removes the schedule timer and doesn't handler the keys"""
        self.paused = True
        self.unschedule(self.step)

    def resume_controller(self):
        """schedules  the timer and handles the keys"""
        self.paused = False
        self.schedule(self.step)

    def step(self, dt):
        """updates the engine"""
        self.elapsed += dt
        if self.elapsed > status.level.speed:
            self.elapsed = 0
            self.model.block_down(sound=False)

    def draw(self):
        """draw the map and the block"""
        self.used_key = False
# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\samples\tetrico\gameover.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 3171 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from pyglet.window import key
from cocos.layer import Layer, ColorLayer
import cocos.director as director
from cocos.text import Label
from cocos.actions import *
import soundex, hiscore, status

class GameOver(ColorLayer):
    is_event_handler = True

    def __init__(self, win=False):
        super(GameOver, self).__init__(32, 32, 32, 64)
        w, h = director.get_window_size()
        if win:
            soundex.play('oh_yeah.mp3')
            msg = 'YOU WIN'
        else:
            soundex.play('no.mp3')
            msg = 'GAME OVER'
        label = Label(msg, font_name='Edit Undo Line BRK',
          font_size=54,
          anchor_y='center',
          anchor_x='center')
        label.position = (w / 2.0, h / 2.0)
        self.add(label)
        angle = 5
        duration = 0.05
        accel = 2
        rot = Accelerate(Rotate(angle, duration // 2), accel)
        rot2 = Accelerate(Rotate(-angle * 2, duration), accel)
        effect = rot + (rot2 + Reverse(rot2)) * 4 + Reverse(rot)
        label.do(Repeat(Delay(5) + effect))
        if hiscore.hiscore.is_in(status.status.score):
            self.hi_score = True
            label = Label('Enter your name:', font_name='Edit Undo Line BRK',
              font_size=36,
              anchor_y='center',
              anchor_x='center',
              color=(32, 32, 32, 255))
            label.position = (
             w / 2.0, h / 2.0)
            label.position = (w // 2, 300)
            self.add(label)
            self.name = Label('', font_name='Edit Undo Line BRK',
              font_size=36,
              anchor_y='center',
              anchor_x='center',
              color=(32, 32, 32, 255))
            self.name.position = (
             w // 2, 250)
            self.add(self.name)
        else:
            self.hi_score = False

    def on_key_press(self, k, m):
        if not self.hi_score:
            if not k == key.ENTER:
                if k == key.ESCAPE:
                    director.pop()
                    return True
        if self.hi_score:
            if k == key.BACKSPACE:
                self.name.element.text = self.name.element.text[0:-1]
                return True
            if k == key.ENTER:
                hiscore.hiscore.add(status.status.score, self.name.element.text, status.status.level_idx)
                director.pop()
                return True
        return False

    def on_text(self, t):
        if not self.hi_score:
            return False
        if t == '\r':
            return True
        self.name.element.text += t
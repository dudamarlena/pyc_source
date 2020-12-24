# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_menu_centered.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1390 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'menu, menu_valign, menu_halign'
from pyglet import image
from pyglet.gl import *
from pyglet import font
from cocos.director import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *

class MainMenu(Menu):

    def __init__(self):
        super(MainMenu, self).__init__('TITLE')
        self.menu_valign = CENTER
        self.menu_halign = CENTER
        items = [
         MenuItem('Item 1', self.on_quit),
         MenuItem('Item 2', self.on_quit),
         MenuItem('Item 3', self.on_quit),
         MenuItem('Item 4', self.on_quit),
         MenuItem('Item 5', self.on_quit),
         MenuItem('Item 6', self.on_quit),
         MenuItem('Item 7', self.on_quit)]
        self.create_menu(items, shake(), shake_back())

    def on_quit(self):
        pyglet.app.exit()


def main():
    pyglet.font.add_directory('.')
    director.init(resizable=True)
    director.run(Scene(MainMenu()))


if __name__ == '__main__':
    main()
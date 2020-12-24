# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_menu_rotated.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1532 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'menu, layout_strategy, fixedPositionMenuLayout'
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from pyglet import font
from pyglet.app import exit
import cocos.director as director
from cocos.menu import Menu, MenuItem, fixedPositionMenuLayout
from cocos.menu import shake, shake_back
from cocos.scene import Scene

class MainMenu(Menu):

    def __init__(self):
        super(MainMenu, self).__init__('TITLE')
        item1 = MenuItem('Item 1', self.on_quit)
        item2 = MenuItem('Item 2', self.on_quit)
        item3 = MenuItem('Item 3', self.on_quit)
        item4 = MenuItem('Item 4', self.on_quit)
        item1.rotation = 45
        item2.rotation = 90
        item3.scale = 2
        item4.scale = 1.5
        item4.rotation = 90
        items = [
         item1, item2, item3, item4]
        self.create_menu(items, layout_strategy=(fixedPositionMenuLayout([
         (450, 300), (130, 200), (200, 100), (400, 50)])))

    def on_quit(self):
        exit()


def main():
    font.add_directory('.')
    director.init(resizable=True)
    director.run(Scene(MainMenu()))


if __name__ == '__main__':
    main()
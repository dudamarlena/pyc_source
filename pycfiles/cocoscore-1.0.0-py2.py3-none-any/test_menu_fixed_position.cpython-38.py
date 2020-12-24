# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_menu_fixed_position.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1367 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'menu, layout_strategy, fixedPositionMenuLayout'
from pyglet import font
from pyglet.app import exit
import cocos.director as director
from cocos.menu import Menu, MenuItem, fixedPositionMenuLayout
from cocos.menu import shake, shake_back
from cocos.scene import Scene

class MainMenu(Menu):

    def __init__(self):
        super(MainMenu, self).__init__('TITLE')
        items = [
         MenuItem('Item 1', self.on_quit),
         MenuItem('Item 2', self.on_quit),
         MenuItem('Item 3', self.on_quit),
         MenuItem('Item 4', self.on_quit)]
        self.create_menu(items, selected_effect=(shake()), unselected_effect=(shake_back()),
          layout_strategy=(fixedPositionMenuLayout([
         (450, 300), (130, 200), (200, 100), (400, 50)])))

    def on_quit(self):
        exit()


def main():
    font.add_directory('.')
    director.init(resizable=True)
    director.run(Scene(MainMenu()))


if __name__ == '__main__':
    main()
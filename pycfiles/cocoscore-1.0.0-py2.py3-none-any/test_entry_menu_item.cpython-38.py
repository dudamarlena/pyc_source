# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_entry_menu_item.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 953 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'EntryMenuItem'
import pyglet
from cocos.director import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *

class MainMenu(Menu):

    def __init__(self):
        super(MainMenu, self).__init__('EntryMenuItem')
        l = []
        l.append(EntryMenuItem('Name:', self.on_name, 'default'))
        l.append(MenuItem('Quit', self.on_quit))
        self.create_menu(l)

    def on_name(self, value):
        print(value)

    def on_quit(self):
        pyglet.app.exit()


def main():
    director.init(resizable=True)
    director.run(Scene(MainMenu()))


if __name__ == '__main__':
    main()
# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_multiplex_layer.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1892 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1.1, s, q'
tags = 'MultiplexLayer'
autotest = 0
import pyglet
from cocos.director import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *
from cocos.actions import Delay, CallFunc

class MainMenu(Menu):

    def __init__(self):
        super(MainMenu, self).__init__('MultiplexLayer')
        l = []
        l.append(MenuItem('Options', self.on_new_game))
        l.append(MenuItem('Quit', self.on_quit))
        self.create_menu(l)
        if autotest:
            self.do(Delay(1) + CallFunc(self.on_new_game))

    def on_new_game(self):
        self.parent.switch_to(1)

    def on_quit(self):
        pyglet.app.exit()


class OptionMenu(Menu):

    def __init__(self):
        super(OptionMenu, self).__init__('MultiplexLayer')
        l = []
        l.append(MenuItem('Fullscreen', self.on_fullscreen))
        l.append(MenuItem('OK', self.on_quit))
        self.create_menu(l)

    def on_fullscreen(self):
        pass

    def on_quit(self):
        self.parent.switch_to(0)


description = "\nDemostrates MultiplexLayer, a layer which can hold many layers, showing\none of them at a time and handling navigation between layers.\nActivate 'Options' to switch to the 'options' layer.\n"

def main():
    print(description)
    director.init(resizable=True)
    scene = Scene(MultiplexLayer(MainMenu(), OptionMenu()))
    director.run(scene)


if __name__ == '__main__':
    main()
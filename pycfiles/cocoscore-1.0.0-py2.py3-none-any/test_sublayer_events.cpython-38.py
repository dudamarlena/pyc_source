# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_sublayer_events.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1921 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 'dt 0.1, q'
tags = 'window event, on_key_press'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
import pyglet

class PrintKey(cocos.layer.Layer):
    is_event_handler = True

    def on_key_press(self, key, modifiers):
        print('Sublayer sees on_key_pressed:', key, modifiers)


class SwitchLayer(cocos.layer.Layer):

    def __init__(self):
        super(SwitchLayer, self).__init__()
        self.other = PrintKey()
        self.added = False

    is_event_handler = True

    def on_key_press(self, key, modifiers):
        print('Layer sees on_key_pressed:', key, modifiers)
        if key == pyglet.window.key.SPACE:
            self.added = not self.added
            print('\nSublayer present:', self.added)
            if self.added:
                self.add(self.other)
            else:
                self.remove(self.other)


description = "\nDemostrates\n    How window events cascade from children to parent.\n    After removing a child from the active scene, it doesn't receive\n    windows events.\n\n    Pressing 'space' will add / remove a sublayer\n\n    When the sublayer is present, pressing any key except 'space' should\n    print two lines, one from the layer and another from the sublayer;\n\n    When the sublayer is not present, pressing any key except 'space' should\n    print one line from the layer.\n"

def main():
    print(description)
    director.init()
    bg_layer = cocos.layer.ColorLayer(255, 0, 0, 255)
    test_layer = SwitchLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()